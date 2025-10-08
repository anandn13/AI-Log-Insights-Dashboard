import os
from elasticsearch import Elasticsearch

ES_HOST = os.getenv('ELASTIC_HOST','localhost')
ES_PORT = os.getenv('ELASTIC_PORT','9200')
ES_INDEX = os.getenv('ELASTIC_INDEX','logs')

es = Elasticsearch(hosts=[{"host": ES_HOST, "port": ES_PORT}])

# ensure index
if not es.indices.exists(index=ES_INDEX):
    es.indices.create(index=ES_INDEX, body={
        "mappings": {
            "properties": {
                "timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "level": {"type": "keyword"},
                "source": {"type": "keyword"},
                "message": {"type": "text"},
                "embedding": {"type":"dense_vector", "dims":384}
            }
        }
    })


def index_log(doc: dict):
    resp = es.index(index=ES_INDEX, document=doc)
    return resp


def search_semantic(query_vector, top_k=5):
    body = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }
    res = es.search(index=ES_INDEX, body=body)
    return res


