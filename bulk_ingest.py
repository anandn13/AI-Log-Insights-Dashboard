from fastapi import APIRouter, Depends, BackgroundTasks
from typing import List
from models.schemas import LogEntry
from services import elasticsearch_client as es_client
from services import embeddings
from services.auth import get_current_user
import time

router = APIRouter()


@router.post('/bulk', dependencies=[Depends(get_current_user)])
def bulk_ingest(entries: List[LogEntry], background_tasks: BackgroundTasks):
    docs = [e.dict() for e in entries]
    texts = [d['message'] for d in docs]
    embs = embeddings.embed_texts(texts)
    for d, emb in zip(docs, embs):
        d['embedding'] = emb
    job = {'count': len(docs), 'status': 'queued'}

    def index_job(docs_batch):
        batch_size = 100
        for i in range(0, len(docs_batch), batch_size):
            batch = docs_batch[i:i+batch_size]
            tries = 0
            while tries < 3:
                try:
                    from elasticsearch import helpers
                    actions = [{'_op_type':'index', '_index': es_client.ES_INDEX, '_source': doc} for doc in batch]
                    helpers.bulk(es_client.es, actions)
                    break
                except Exception:
                    tries += 1
                    time.sleep(2 ** tries)
                    if tries >= 3:
                        print('Bulk index failed for batch')

    background_tasks.add_task(index_job, docs)
    return {'job_id': 'bg-'+str(int(time.time())), 'status': 'accepted'}


