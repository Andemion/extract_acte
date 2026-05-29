from datetime import datetime

from tools.es_service.es_query_preparer import treatment_response

import tools.es_service.es_query_dictionnary as es_dict


async def call_to_opensearch(open_search_client_v2, inot_ids, logger):

    url = "sous_dossiers/_doc/id:" + str(inot_ids["dossierId"]) + "_tenantId:" + str(inot_ids["tenantId"])
    inot_result = open_search_client_v2.execute_query_by_url(url)

    if "error" in inot_result:
        return inot_result

    return serialise_inot_to_wemblee(open_search_client_v2, inot_result, inot_ids, logger)

def serialise_inot_to_wemblee(open_search_client_v2, inot_response, inot_ids, logger):
    logger.info("Starting serialisation of iNot response for FileS3Id: %s", inot_ids["fileS3Id"])

    # Initialisation de la réponse JSON
    json_response = {
        "dateSignature": "",
        "notaires": [],
        "parties": [],
        "adresse": "",
        "typeBien": "",
        "nature": ""
    }
    logger.debug("Initial JSON response structure: %s", json_response)

    try:
        # Étape 1 : Récupération de la date de l'acte
        logger.info("Fetching iNot document for FileS3Id: %s", inot_ids["fileS3Id"])
        document_query = es_dict.find_inot_document_query
        document_query["query"]["bool"]["must"][0]["term"]["s3Id.keyword"] = inot_ids["fileS3Id"]
        open_search_client_v2.set_index_name("documents")

        inot_document = treatment_response(open_search_client_v2, document_query)
        logger.debug("iNot document fetched successfully: %s", inot_document)

        date_obj = datetime.strptime(inot_document[0]["_source"]["dateCreation"], "%Y-%m-%dT%H:%M:%S")
        json_response["dateSignature"] = date_obj.strftime("%d/%m/%Y")
        logger.info("Date of signature set successfully: %s", json_response["dateSignature"])
    except Exception as e:
        logger.exception("Error while fetching the iNot document or parsing the date: %s", e)
        raise

    # Étape 2 : Traitement des immeubles
    if "immeubles" in inot_response:
        if  len(inot_response["immeubles"]) > 0:
            logger.info(f"Processing 'immeubles' from iNot response: {inot_response['immeubles']}.")
            try:
                json_response["adresse"] = concat_adresses(inot_response["immeubles"][0]["adresse"])
                json_response["typeBien"] = inot_response["immeubles"][0]["nature"]["intitule"]
                logger.info("Immeuble processed successfully: Adresse=%s, TypeBien=%s",
                            json_response["adresse"], json_response["typeBien"])
            except Exception as e:
                logger.exception("Error while processing 'immeubles' in iNot response: %s", e)

    # Étape 3 : Traitement des notaires et clercs
    for role in ["notaire", "clerc"]:
        if role in inot_response and inot_response[role] is not None:
            logger.info("Processing '%s' from iNot response.", role.capitalize())
            try:
                inot_person = inot_response[role]["identite"].split(" ")
                sorted_person = sort_names(inot_person)
                sorted_person.update({"etude": inot_ids["tenantName"], "type": role}) #"adresse": None
                json_response["notaires"].append(sorted_person)
                logger.debug("Added %s to 'notaires': %s", role, sorted_person)
            except Exception as e:
                logger.exception("Error while processing '%s': %s", role, e)

    # Étape 4 : Traitement des partenaires
    if "partenaires" in inot_response:
        if inot_response["partenaires"] is not None and len(inot_response["partenaires"]) > 0:
            logger.info("Processing 'partenaires' from iNot response.")
            try:
                for partenaire in inot_response["partenaires"]:
                    if partenaire["civilite"]["intitule"] == "Maître":
                        notaire = {
                            "nom": partenaire["nom"],
                            "prenom": partenaire["prenom"],
                            "etude": None,
                            "adresse": None,
                            "type": "notaire_partenaires"
                        }
                        json_response["notaires"].append(notaire)
                        logger.debug("Added 'partenaire' to 'notaires': %s", notaire)
            except Exception as e:
                logger.exception("Error while processing 'partenaires': %s", e)

    # Étape 5 : Traitement des comparants
    if "comparants" in inot_response:
        if inot_response["comparants"] is not None and len(inot_response["comparants"]) > 0:
            logger.info("Processing 'comparants' from iNot response.")
            try:
                for comparant in inot_response["comparants"]:
                    partie = {}
                    if comparant["typeComparant"] == "ClientPhysique":
                        logger.info("Fetching 'ClientPhysique' comparant details.")
                        url_comparant = (
                                "clients_physiques/_doc/id:" + str(comparant["idComparantPrincipal"]) +
                                "_tenantId:" + str(inot_ids["tenantId"])
                        )
                        inot_comparant = open_search_client_v2.execute_query_by_url(url_comparant)

                        if "error" in inot_comparant:
                            logger.error("Error fetching 'ClientPhysique' comparant data: %s", inot_comparant)
                            return inot_comparant

                        comparant_names = inot_comparant["denomination"].split(" ")
                        partie = partie | sort_names(comparant_names)
                        partie.update({
                            "adresse": concat_adresses(inot_comparant["adresse"]),
                            "dateDeNaissance": f'{inot_comparant["dateNaissance"]["jour"]}/'
                                               f'{inot_comparant["dateNaissance"]["mois"]}/'
                                               f'{inot_comparant["dateNaissance"]["annee"]}',
                            "situationFamiliale": inot_comparant["etatMarital"]["intitule"],
                            "nationalite": None,
                            "type": comparant["qualite"]["intitule"]
                        })
                        logger.debug("Added 'ClientPhysique' comparant to 'parties': %s", partie)
                    else:
                        logger.info("Fetching 'ClientMoral' comparant details.")
                        url_comparant = (
                                "clients_moraux/_doc/id:" + str(comparant["idComparantPrincipal"]) +
                                "_tenantId:" + str(inot_ids["tenantId"])
                        )
                        inot_comparant = open_search_client_v2.execute_query_by_url(url_comparant)

                        partie = {
                            "nom": inot_comparant["denomination"],
                            "adresse": concat_adresses(inot_comparant["adresse"]),
                            "formeJuridique": inot_comparant["formeSociete"]["intitule"],
                            "capital": None,
                            "registre": inot_comparant["registreCommerce"],
                            "siren": inot_comparant["siren"],
                            "type": comparant["qualite"]["intitule"]
                        }
                        logger.debug("Added 'ClientMoral' comparant to 'parties': %s", partie)

                    json_response["parties"].append(partie)
            except Exception as e:
                logger.exception("Error while processing 'comparants': %s", e)

    # Étape 6 : récupération nature du dossier
    if "nature" in inot_response:
        logger.info("Processing 'nature' from iNot response.")
        try:
            json_response["nature"] = inot_response["nature"]
        except Exception as e:
            logger.exception("Error while processing 'natureDossier': %s", e)

    logger.info("iNot serialisation completed successfully for FileS3Id: %s", inot_ids["fileS3Id"])
    logger.debug("Final JSON response: %s", json_response)
    return json_response


def sort_names(person):
    person_familly_name = ""
    person_first_name = ""

    for name in person:
        if name.isupper():
            person_familly_name += name + " "
        else:
            person_first_name += name + " "

    return {"nom": person_familly_name.rstrip(), "prenom": person_first_name.rstrip()}


def concat_adresses(inot_adress):

    numero = ""
    extension_numero = ""
    type_voie = ""
    voie = ""
    code_postal = ""
    commune = ""
    complement_adresse = ""
    pays = ""

    if "numero" in inot_adress:
        if inot_adress["numero"]:
            numero = inot_adress["numero"] + " "

    if "extensionNumero" in inot_adress:
        if inot_adress["extensionNumero"]:
            if inot_adress["extensionNumero"]["intitule"]:
                extension_numero = inot_adress["extensionNumero"]["intitule"] + " "

    if "typeVoie" in inot_adress:
        if inot_adress["typeVoie"]:
            if inot_adress["typeVoie"]["intitule"]:
                type_voie = inot_adress["typeVoie"]["intitule"] + " "

    if "voie" in inot_adress:
        if inot_adress["voie"]:
            voie = inot_adress["voie"] + " "

    if "commune" in inot_adress:
        if inot_adress["commune"]["codePostal"]:
            code_postal = inot_adress["commune"]["codePostal"] + " "
        if inot_adress["commune"]["nom"]:
            commune = inot_adress["commune"]["nom"] + " "

    if "complementAdresse" in inot_adress:
        if inot_adress["complementAdresse"]:
            complement_adresse = inot_adress["complementAdresse"] + " "

    if "pays" in inot_adress:
        if inot_adress["pays"]:
            if inot_adress["pays"]["intitule"]:
                pays = inot_adress["pays"]["intitule"]

    return numero + extension_numero + type_voie + voie + complement_adresse + code_postal + commune + pays
