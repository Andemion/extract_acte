range_query = {
    "size": 0,
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "fileS3Id.keyword": ""
                    }
                }
            ],
            "must_not": [
                {
                    "term": {
                        "text.keyword": ""
                    }
                }
            ],
            "should": [
                {
                    "range": {
                        "page_number": {
                            "gt": 0,
                            "lt": 0
                        }
                    }
                }
            ],
            "minimum_should_match": 1
        }
    },
    "aggs": {
        "unique_pages": {
            "terms": {
                "script": {
                    "source": "doc['page_number'].value + '_' + doc['type.keyword'].value",
                    "lang": "painless"
                },
                "size": 100
            },
            "aggs": {
                "top_hits": {
                    "top_hits": {
                        "size": 1
                    }
                }
            }
        }
    }
}

find_words_query = {
    "size": 200,
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "fileS3Id.keyword": ""
                    }
                }
            ],
            "should": [],
            "minimum_should_match": 0,
            "must_not": []
        }
    },
    "sort": [
        {
            "page_number": {
                "order": "asc"
            }
        },
        {
            "block_number": {
                "order": "asc"
            }
        }
    ]
}

find_inot_document_query = {
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "s3Id.keyword": ""
                    }
                }
            ]
        }
    }
}