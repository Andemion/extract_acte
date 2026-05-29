import copy

import tools.es_service.es_query_dictionnary as query_dictionnary

from operator import itemgetter


def query_range_es(open_search_client, fileS3Id, requested_object, page_number=0):

    before_page_number = 0
    after_page_number = 0

    for object2find in requested_object:
        # pareil que dans le code appelant, des 'in' dans des sets pour la lisibilité
        if object2find in {"donation"}:
            before_page_number = 0
            after_page_number = 20
            break

        elif object2find in {"dateSignature", "notaires", "parties", "family"}:
            before_page_number = 0
            after_page_number = 6
            break

        elif object2find in {"immeubles", "adresse", "conditions_suspensives", "natureFromContent"} :
            before_page_number = page_number - 1
            after_page_number = page_number + 1

        elif object2find in {"prixVente", "paiementPrix", "origineFond", "pret", "donation"}:
            before_page_number = page_number - 1
            after_page_number = page_number + 4
            break

    query_range = query_dictionnary.range_query
    query_range['query']['bool']['must'][0]['term']['fileS3Id.keyword'] = fileS3Id
    query_range['query']['bool']['should'][0]['range']['page_number']['gt'] = before_page_number
    query_range['query']['bool']['should'][0]['range']['page_number']['lt'] = after_page_number

    return treatment_response(open_search_client, query_range)


def query_words_es(open_search_client, fileS3Id, words, logger, no_words=None):

    if no_words is None:
        no_words = []
    """return only the block_number of the title"""
    query = copy.deepcopy(query_dictionnary.find_words_query)
    query['query']['bool']['must'][0]['term']['fileS3Id.keyword'] = fileS3Id
    query['query']['bool']['should'].clear()
    for word in words:
        query['query']['bool']['should'].append({
            "match": {
                "text": {
                    "query": word,
                    "fuzziness": 4
                }
            }
        })

    if len(no_words) > 0:
        query['query']['bool']['must_not'].append(
            {
                "span_near": {
                    "clauses": [],
                    "slop": 1,
                    "in_order": True
                }
            })
        for no_word in no_words:
            query['query']['bool']['must_not'][0]["span_near"]["clauses"].append(
                {
                    "span_multi": {
                        "match": {
                            "fuzzy": {
                                "text": {
                                    "value": no_word,
                                    "fuzziness": "auto"
                                }
                            }
                        }
                    }
                }
            )

    query['query']['bool']['minimum_should_match'] = 1

    return treatment_response(open_search_client, query)


def treatment_response(open_search_client, query):

    response = open_search_client.search_documents(query)

    if isinstance(response, dict):
        if "aggregations" in response.keys():
            get_hits = []
            for hits in response['aggregations']['unique_pages']['buckets']:
                get_hits.append(hits['top_hits']['hits']['hits'][0]['_source'])
            return sorted(get_hits, key=itemgetter("page_number", "type"))

    return response["hits"]["hits"]
