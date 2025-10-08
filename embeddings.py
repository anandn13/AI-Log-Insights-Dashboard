import os
from typing import List

USE_LOCAL = os.getenv('USE_LOCAL_EMBEDDINGS','true').lower() in ('true','1')
LOCAL_MODEL = os.getenv('LOCAL_EMBEDDINGS_MODEL','all-MiniLM-L6-v2')

if USE_LOCAL:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(LOCAL_MODEL)
    def embed_texts(texts: List[str]):
        emb = model.encode(texts, show_progress_bar=False)
        return emb.tolist()
else:
    from langchain.embeddings import OpenAIEmbeddings
    oe = OpenAIEmbeddings()
    def embed_texts(texts: List[str]):
        return [oe.embed_query(t) for t in texts]


