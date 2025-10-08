from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from services import embeddings_switch
from services.elasticsearch_client import es
from sklearn.ensemble import IsolationForest
import numpy as np


class ESRetriever:
    def __init__(self, index_name='logs'):
        self.index = index_name

    def get_relevant(self, query, top_k=5):
        qvec = embeddings_switch.embed_texts([query])[0]
        res = es.search(index=self.index, body={
            'size': top_k,
            'query': {
                'script_score': {
                    'query': {'match_all': {}},
                    'script': {'source': "cosineSimilarity(params.query_vector, 'embedding') + 1.0", 'params': {'query_vector': qvec}}
                }
            }
        })
        hits = [h['_source'] for h in res['hits']['hits']]
        return hits


def build_rag_chain(openai_api_key=None):
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
    prompt = PromptTemplate(input_variables=['context','question'], template='''You are an assistant. Use the context to answer the question.
Context:
{context}
Question: {question}
Answer concisely.''')

    def rag_run(question):
        retr = ESRetriever()
        docs = retr.get_relevant(question, top_k=5)
        context = '\n'.join([d.get('message','') for d in docs])
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run({'context': context, 'question': question})

    return rag_run


def detect_anomalies_from_embeddings(embeddings_list):
    if len(embeddings_list) < 10:
        return []
    X = np.array(embeddings_list)
    iso = IsolationForest(contamination=0.01, random_state=42)
    preds = iso.fit_predict(X)
    anomalies = np.where(preds == -1)[0].tolist()
    return anomalies


