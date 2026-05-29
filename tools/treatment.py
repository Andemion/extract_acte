import threading
import time

from tools.treatment_response import *
from tools.es_service.es_query_preparer import *
from tools.chatGPT.ChatGptTools import question_2_chatgpt


async def threading_treatment(open_search_client, fileS3Id, requested_object, logger, model):
    immeubles = {}
    conditions_suspensives = {}
    prix = {}
    comparants = {}
    threads = []
    sign_block_requested = []
    immeuble_bloc = []
    price_bloc = []

    '''Make fusion of the requested_object how come from the same part of the text to save some token'''
    for requested in requested_object:
        # on utilise des 'in' dans des set pour gagner du temps de comparaison et surtout de la lisibilité
        if requested in {"dateSignature", "notaires", "parties", "family", "donation" }:
            sign_block_requested.append(requested)
        elif requested in {"immeubles", "adresse", "natureFromContent"}:
            immeuble_bloc.append(requested)
        elif requested in {"prixVente", "paiementPrix", "origineFond", "pret"}:
            price_bloc.append(requested)

    start = time.perf_counter()

    if sign_block_requested:
        t1 = threading.Thread(
            target=get_response_sign_block,
            args=(open_search_client, sign_block_requested, fileS3Id, comparants, logger, model)
        )
        t1.start()
        threads.append(t1)

    if immeuble_bloc:
        t2 = threading.Thread(
            target=get_response_immeuble_block,
            args=(open_search_client, immeuble_bloc, fileS3Id, immeubles, logger, model)
        )
        t2.start()
        threads.append(t2)

    if "conditions_suspensives" in requested_object:
        t3 = threading.Thread(
            target=get_response_conditions_suspensive_block,
            args=(open_search_client, ["conditions_suspensives"], fileS3Id, conditions_suspensives, logger, model)
        )
        t3.start()
        threads.append(t3)

    if price_bloc:
        t4 = threading.Thread(
            target=get_response_prix_block,
            args=(open_search_client, price_bloc, fileS3Id, prix, logger, model)
        )
        t4.start()
        threads.append(t4)

    for thread in threads:
        thread.join()

    finish = time.perf_counter()
    logger.info(f'Finish all treatments in {round(finish - start, 2)} second(s)')

    return comparants | immeubles | conditions_suspensives | prix


def get_response_sign_block(open_search_client, requested_object, fileS3Id, json_response, logger, model):
    gpt_response = {}

    range_response = query_range_es(open_search_client, fileS3Id, requested_object)
    if not range_response:
        json_response.update({"error": True, "message": 'No data found in Elasticsearch'})
        return

    call_to_chatgpt(range_response, requested_object, gpt_response, logger, model)

    json_response.update(sign_block_treatment(gpt_response))


def get_response_immeuble_block(open_search_client, requested_object, fileS3Id, json_response, logger, model):

    texte_pages = ""
    words = ["designation", "cadastre", "volume", "lot", "mariage", "divorce", "donation", "succession" ]
    result = query_words_es(open_search_client, fileS3Id, words, logger)
    if not result:
        json_response.update({"error": True, "message": 'No data found for immeuble in Elasticsearch'})
        return

    previous_page = 0
    for hit in result:
        page = int(hit["_source"]["page_number"])
        if page > 25:
            break
        hits = query_range_es(open_search_client, fileS3Id, requested_object, page)
        for h in hits:
            if previous_page != page:
                logger.info(f"Texte page {page}")
                previous_page = page
                texte_pages += "--- Texte page " + str(page) + " --- " + h["text"] + " "

    gpt_response = {}

    try:
        call_to_chatgpt(texte_pages, requested_object, gpt_response, logger, model)

        if "immeubles" in requested_object:
            json_response.update(parcelle_block_treatment(gpt_response))
        else:
            json_response.update(gpt_response)
    except:
        json_response.update({"error": True, "message": "Post ChatGPT PARCELLE_BLOCK treatment failed."})


def get_response_conditions_suspensive_block(open_search_client, requested_object, fileS3Id, json_response, logger, model):
    texte_pages = ""
    words = ["suspensive", "condition", "délai"]
    no_words = ["delai", "previsionnel", "de", "realisation", "des", "conditions"]
    result = query_words_es(open_search_client, fileS3Id, words, logger, no_words)
    if not result:
        json_response.update({"error": True, "message": 'No data found for conditions_suspensives in Elasticsearch'})
        return

    previous_page = 0
    for hit in result:
        page = int(hit["_source"]["page_number"])
        hits = query_range_es(open_search_client, fileS3Id, requested_object, page)
        for h in hits:
            if previous_page != page:
                previous_page = page
                texte_pages += "--- Texte page " + str(page) + " --- " + h["text"] + " "
            else:
                texte_pages += h["text"] + " "

    call_to_chatgpt(texte_pages, requested_object, json_response, logger, model)


def get_response_prix_block(open_search_client, requested_object, fileS3Id, json_response, logger, model):
    texte = ""
    words = ["prix", "vente", "moyennant"]
    result = query_words_es(open_search_client, fileS3Id, words, logger)

    if not result:
        json_response.update({"error": True, "message": 'No data found for price in Elasticsearch'})
        return

    for hit in result:
        page = int(hit["_source"]["page_number"])
        hits = query_range_es(open_search_client, fileS3Id, requested_object, page)
        for h in hits:
            texte += h["text"] + " "

    call_to_chatgpt(texte, requested_object, json_response, logger, model)


def call_to_chatgpt(hits, requested_object, response, logger, model):

    text = ""

    if isinstance(hits, list):
        for hit in hits:
            text += hit["text"] + " "
    elif isinstance(hits, str):
        text = hits
    else:
        text += hits["text"] + " "

    if text != "":
        question_2_chatgpt(text, requested_object, response, logger, model)
    else:
        response.update({"error": True, "message": f"Empty text for {requested_object}"})
