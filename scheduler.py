from apscheduler.schedulers.background import BackgroundScheduler
from services.langchain_chains import build_rag_chain, detect_anomalies_from_embeddings
from services.elasticsearch_client import es
from services import embeddings_switch
import os


def job_daily_summary():
    res = es.search(index=os.getenv('ELASTIC_INDEX','logs'), body={'size':1000, 'query': {'range': {'timestamp': {'gte': 'now-24h'}}}})
    hits = [h['_source'] for h in res['hits']['hits']]
    messages = [h.get('message','') for h in hits]
    emb = embeddings_switch.embed_texts(messages) if messages else []
    anomalies = detect_anomalies_from_embeddings(emb)
    rag = build_rag_chain(openai_api_key=os.getenv('OPENAI_API_KEY'))
    summary = rag('Provide a short daily summary of the following logs:') if len(messages) else 'No logs'
    es.index(index=os.getenv('ELASTIC_INDEX','logs'), document={'timestamp': 'now', 'level':'INFO','source':'scheduler','message': summary, 'meta': {'anomalies': anomalies}})


def start_scheduler():
    sched = BackgroundScheduler()
    sched.add_job(job_daily_summary, 'interval', hours=24)
    sched.start()


