import tornado.ioloop
import pydevd_pycharm
import sys
import json

from tornado.web import RequestHandler

from tools.treatment import threading_treatment
from tools.inot_serializer import call_to_opensearch

from shared.AWS.lambda_authentication import check_aws_secret
from shared.Logger.logger import get_logger
from shared.AWS.init_session_and_clients import *

"""----------------This line is use to debbug check README for more details--------------------------"""
sys.path.append("./debug/pydevd-pycharm.egg")
pydevd_pycharm.settrace('host.docker.internal', port=5681, stdoutToServer=True, stderrToServer=True)
"""--------------------------------------------------------------------------------------------------"""

# Initialisation de tous les clients nécessaires à cette lambda
logger = get_logger(__name__)
logger.info("Logger initialized successfully")
aws_session = get_session(logger)
open_search_client_v2 = get_open_search_client_v2("", logger)
secret_manager_client = get_secret_manager_client(aws_session)
s3_client = get_s3_client(aws_session, logger)


class DevEntrypoint(RequestHandler):

    async def post(self):
        self.set_header('Content-type', 'application/json')
        event = {"body": self.request.body, "headers": self.request.headers._dict}

        body = event.get('body')
        headers = event.get('headers', {})

        # Convertir les clés d'en-tête en minuscules pour éviter les problèmes de casse
        headers = {k.lower(): v for k, v in headers.items()}

        # Vérification de la présence de l'en-tête 'api-key'
        if 'api-key' not in headers:
            logger.error("No api-key in headers")
            return self.send_response(401, {'message': 'API key missing'})

        api_key = headers['api-key']
        if not check_aws_secret(api_key, secret_manager_client, logger):
            logger.error("Bad secret key")
            return self.send_response(401, {'message': 'Bad secret key'})

        return await self.generic_process_message(json.loads(body), "http")

    async def generic_process_message(self, request_params, request_type):

        try:
            bucket = request_params['bucket']
            fileS3Id = request_params['fileS3Id']
            es_index = request_params['es_index']
            requested_object = request_params['requested_object']
        except KeyError as k:
            logger.error(f"KeyError: {k}")
            return self.send_response(400, {
                'message': "Bad request body ! ",
                "Required parameters": "'bucket', 'fileS3Id', 'es_index', 'requested_object'.",
                "requested_object possibility": "'dateSignature', 'notaires', 'parties', 'immeubles', 'family', 'natureFromContent', 'adresse', 'conditions_suspensives', 'prixVente', 'paiementPrix', 'origineFond', 'pret'"
            })

        try:
            json_response = {}
            llm = True

            object_metier_id = request_params.get('objectMetierId', None)
            model = request_params.get('model', "ChatGPT")

            if "source" in request_params:
                if request_params["source"]["name"] == "iNot":
                    llm = False
                    await self.call_inot_serializer(open_search_client_v2, request_params["source"], logger, json_response)
                    complete_objects_with_llm = []

                    if json_response["adresse"] == "":
                        complete_objects_with_llm.append("adresse")
                    if "natureFromContent" in requested_object:
                        complete_objects_with_llm.append("natureFromContent")

                    if len(complete_objects_with_llm) > 0:
                        llm = True
                        requested_object = complete_objects_with_llm
            if llm:
                open_search_client = get_open_search_client_v2(es_index, logger)
                if len(requested_object) == 0:
                    requested_object = ["dateSignature", "notaires", "parties", "family",
                                        "immeubles", "adresse", "natureFromContent",
                                        "conditions_suspensives",
                                        "prixVente", "paiementPrix", "origineFond", "pret"]

                await self.serialize_coroutine_to_json(open_search_client, fileS3Id, requested_object, logger, model, json_response)

                final_keys = json_response.keys()
                if "natureFromContent" in final_keys:
                    # Initialiser "nature" si elle n'existe pas
                    if "nature" not in json_response:
                        json_response["nature"] = ""

                    for nat in json_response["natureFromContent"]:
                        json_response["nature"] +=  " / " + nat

                    json_response.pop("natureFromContent")

            logger.info(f"Preparing payload to return with request_type : {request_type}")
            pre_signed_url = s3_client.create_presigned_url(bucket, fileS3Id)
            result = {"preSignedUrl": pre_signed_url, "objectMetierId": object_metier_id} | json_response

            return self.send_response(200, result)

        except Exception as e:
            logger.error(f"Exception: {e}")
            return self.send_response(400, {"message": f"error : {e}"})

    @staticmethod
    async def serialize_coroutine_to_json(open_search_client, fileS3Id, requested_object, logger, model, json_response):

        result = await threading_treatment(open_search_client, fileS3Id, requested_object, logger, model)

        # Vérifiez que la liste result contient au moins un élément
        if not result or not isinstance(result, dict):
            logger.error("Serialization result is empty or invalid: %s", result)
            raise ValueError("Serialization result is empty or invalid")

        json_response.update(result)
        logger.info("Serialization to JSON completed successfully.")

    @staticmethod
    async def call_inot_serializer(open_search_client_v2, inot_ids, logger, json_response):

        result = await call_to_opensearch(open_search_client_v2, inot_ids, logger)

        # Vérifiez que la liste result contient des données
        if not result or not isinstance(result, dict):
            logger.error("iNot serialization result is empty or invalid: %s", result)
            raise ValueError("iNot serialization result is empty or invalid")

        json_response.update(result)
        logger.info("iNot serialization completed successfully.")

    def send_response(self, status_code, body):
        self.set_status(status_code)
        self.write(body)


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", DevEntrypoint),
    ], )

    app.listen(int(os.getenv('PORT_EXPOSED')))

tornado.ioloop.IOLoop.current().start()
