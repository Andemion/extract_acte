import asyncio
import json

from tools.treatment import threading_treatment
from tools.inot_serializer import call_to_opensearch

from shared.Logger.logger import get_logger
from shared.AWS.init_session_and_clients import *
from shared.AWS.lambda_authentication import check_aws_secret

# Initialisation de tous les clients nécessaires à cette lambda
logger = get_logger(__name__)
logger.info("Logger initialized successfully")
aws_session = get_session(logger)
open_search_client_v2 = get_open_search_client_v2("", logger)
secret_manager_client = get_secret_manager_client(aws_session)
s3_client = get_s3_client(aws_session, logger)
sqs_client = get_sqs_client(aws_session, logger)
kinesis_client = get_kinesis_client(aws_session, logger)

def lambda_handler(event, context):
    logger.info(f"Événement reçu : {json.dumps(event)}")
    # Si l'événement vient de SQS
    if "Records" in event:
        for record in event["Records"]:
            message_body = json.loads(record["body"])
            logger.info(f"Message reçu depuis SQS : {json.dumps(message_body)}")
            generic_process_message(message_body, "sqs")
    # Sinon c'est une requête HTTP
    else:
        return process_http_request(event)

def process_http_request(event):
    logger.info("Event: %s", json.dumps(event))
    body = event.get('body')  # Ne définissez pas de valeur par défaut ici
    headers = event.get('headers', {})  # Fournir un dictionnaire vide comme valeur par défaut

    logger.info("headers: %s", json.dumps(headers))

    # Convertir les clés d'en-tête en minuscules pour éviter les problèmes de casse
    headers = {k.lower(): v for k, v in headers.items()}

    # Vérification de la présence de l'en-tête 'api-key'
    if 'api-key' not in headers:
        logger.error("No api-key in headers")
        return send_response(401, {'message': 'API key missing'})

    api_key = headers['api-key']
    if not check_aws_secret(api_key, secret_manager_client, logger):
        logger.error("Bad secret key")
        return send_response(401, {'message': 'Bad secret key'})

    return generic_process_message(json.loads(body), "http")

def generic_process_message(request_params, request_type):

    try:
        bucket = request_params['bucket']
        fileS3Id = request_params['fileS3Id']
        es_index = request_params['es_index']
        requested_object = request_params['requested_object']

    except KeyError as k:
        logger.error(f"KeyError: {k}")
        return send_response(400, {
            'message': "Bad request body ! ",
            "Required parameters": "'bucket', 'fileS3Id', 'es_index', 'requested_object'.",
            "requested_object possibility": "'dateSignature', 'notaires', 'parties', 'immeubles', 'family', 'adresse', 'conditions_suspensives', 'prixVente', 'paiementPrix', 'origineFond', 'pret'"
        })
    try:
        json_response = {}
        llm = True

        object_metier_id = request_params.get('objectMetierId', None)
        model = request_params.get('model', "ChatGPT")
        use_case_json = request_params.get('use_case_json', {})

        if "source" in request_params:
            if request_params["source"]["name"] == "iNot":
                llm = False
                call_inot_serializer(open_search_client_v2, request_params["source"], logger, json_response)
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

            serialize_coroutine_to_json(open_search_client, fileS3Id, requested_object, logger, model, json_response)

            final_keys = json_response.keys()
            if "natureFromContent" in final_keys:
                # Initialiser "nature" si elle n'existe pas
                if "nature" not in json_response:
                    json_response["nature"] = ""

                for nat in json_response["natureFromContent"]:
                    json_response["nature"] +=  " / " + nat

                json_response.pop("natureFromContent")

        logger.info(f"Preparing payload to return with request_type : {request_type}")


        if request_type == "sqs":
            if use_case_json["use_case"] == "rd_wemblee":
                json_response.update({"objectMetierId": object_metier_id})
            kinesis_payload = {
                "error": False,
                "message_type": "extract_acte_response",  # champ sur lequel les filtres de trigger kinesis font leur test
                "use_case_json": use_case_json,
                "result": json_response
            }
            logger.info(f"Payload for kinesis: {kinesis_payload}")
            kinesis_client.publish_kinesis_event_with_backoff(kinesis_payload)
        else:
            pre_signed_url = s3_client.create_presigned_url(bucket, fileS3Id)
            result = {"preSignedUrl": pre_signed_url} | json_response
            return send_response(200, result)

    except Exception as e:
        logger.error(f"Exception: {e}")
        return send_response(400, {"message": f"error : {e}"})


# Fonction pour multi-threading et sérialiser un objet coroutine en JSON
def serialize_coroutine_to_json(open_search_client, fileS3Id, requested_object, logger, model, json_response):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        asyncio.gather(threading_treatment(open_search_client, fileS3Id, requested_object, logger, model))
    )

    # Vérifiez que la liste result contient au moins un élément
    if not result or not isinstance(result, list) or len(result) == 0:
        logger.error("Serialization result is empty or invalid: %s", result)
        raise ValueError("Serialization result is empty or invalid")

    json_response.update(result[0])
    logger.info("Serialization to JSON completed successfully.")


def call_inot_serializer(open_search_client, inot_ids, logger, json_response):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        asyncio.gather(call_to_opensearch(open_search_client, inot_ids, logger))
    )

    # Vérifiez que la liste result contient des données
    if not result or not isinstance(result, list) or len(result) == 0:
        logger.error("iNot serialization result is empty or invalid: %s", result)
        raise ValueError("iNot serialization result is empty or invalid")

    json_response.update(result[0])
    logger.info("iNot serialization completed successfully.")


def send_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
