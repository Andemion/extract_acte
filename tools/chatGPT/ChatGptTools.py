import json
import copy

from tools.chatGPT import schema_dictionary as s
from tools.chatGPT import question_dictionary as q

from shared.ChatGPT.chat_gpt_call import call_2_gpt
from shared.Mistral.mistral_call import call_2_mistral


def question_2_chatgpt(text: str, requested_object: list, response_data, logger, model, second_call=False, retour="") -> json:
    function = [{"name": "", "parameters": {}}]
    question = "Prompt : \n" + q.contexte
    prompt_return = ""
    schema = copy.deepcopy(s.base_schema)

    for object2find in requested_object:

        if object2find == "dateSignature":
            question += q.dateSignature
            schema["properties"].update(s.dateSignature)

        elif object2find == "notaires":
            question += q.notaires
            schema["properties"].update(s.notaires)

        elif object2find == "parties":
            question += q.parties
            schema["properties"].update(s.parties)

        elif object2find == "natureFromContent":
            question += q.natureFromContent
            schema["properties"].update(s.natureFromContent)

        elif object2find == "immeubles":
            question += q.immeubles
            schema["properties"].update(s.immeubles)

        elif object2find == "adresse":
            question += q.adresse
            schema["properties"].update(s.adresse)

        elif object2find == "conditions_suspensives":
            question += q.condition_definition + q.conditions_suspensives
            schema["properties"].update(s.conditions_suspensives)

        elif object2find == "prixVente":
            question += q.price_definition + q.prixVente
            schema["properties"].update(s.prixVente)

        elif object2find == "paiementPrix":
            question += q.paiementPrix
            schema["properties"].update(s.paiementPrix)

        elif object2find == "origineFond":
            question += q.origineFond
            schema["properties"].update(s.origineFond)

        elif object2find == "family":
            question += q.family
            schema["properties"].update(s.family)

        elif object2find == "donation":
            question += q.donation
            schema["properties"].update(s.donation)

        elif object2find == "pret":
            question += q.pret
            schema["properties"].update(s.pret)
            required = ["pret", "detailPret"]
            schema["required"] = required

        if object2find != "pret":
            schema["required"].append(object2find)

    function[0]["name"] = "get" + requested_object[0]
    function[0]["parameters"] = schema

    question += q.end_contexte

    if model == "ChatGPT":
        response_data.update(call_2_gpt(logger, question, text, function, second_call, prompt_return, retour))
    elif model == "Mistral":
        response_data.update(call_2_mistral(logger, question, text, function, second_call, prompt_return, retour))
