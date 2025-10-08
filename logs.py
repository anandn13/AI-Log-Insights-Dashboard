from fastapi import APIRouter, HTTPException
from models.schemas import LogEntry, IngestResponse
from services import elasticsearch_client as es_client
from services import embeddings
from services.langchain_agent import analyze_logs_with_llm
import uuid
import os

router = APIRouter()


@router.post('/ingest', response_model=IngestResponse)
def ingest_log(entry: LogEntry):
    doc = entry.dict()
    emb = embeddings.embed_texts([doc['message']])[0]
    doc['embedding'] = emb
    doc_id = str(uuid.uuid4())
    doc['_id'] = doc_id
    resp = es_client.index_log(doc)
    return IngestResponse(id=resp['_id'], indexed=True)


@router.post('/analyze')
def analyze_bulk(logs: list[LogEntry]):
    texts = "\n".join([f"[{l.timestamp}] {l.level} {l.source or ''} - {l.message}" for l in logs])
    api_key = os.getenv('OPENAI_API_KEY')
    try:
        out = analyze_logs_with_llm(texts, openai_api_key=api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"analysis": out}


@router.get('/search')
def semantic_search(q: str, k: int = 5):
    qvec = embeddings.embed_texts([q])[0]
    res = es_client.search_semantic(qvec, top_k=k)
    hits = [h['_source'] for h in res['hits']['hits']]
    return {"results": hits}


