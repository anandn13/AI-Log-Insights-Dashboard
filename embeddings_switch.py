import os
from typing import List

EMBED_PROVIDER = os.getenv('EMBED_PROVIDER','local')  # local | openai | pinecone

if EMBED_PROVIDER == 'local':
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(os.getenv('LOCAL_EMBEDDINGS_MODEL','all-MiniLM-L6-v2'))
    def embed_texts(texts: List[str]):
        return model.encode(texts, show_progress_bar=False).tolist()

elif EMBED_PROVIDER == 'openai':
    from langchain.embeddings import OpenAIEmbeddings
    oe = OpenAIEmbeddings()
    def embed_texts(texts: List[str]):
        return [oe.embed_query(t) for t in texts]

elif EMBED_PROVIDER == 'pinecone':
    import pinecone
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(os.getenv('LOCAL_EMBEDDINGS_MODEL','all-MiniLM-L6-v2'))
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENV = os.getenv('PINECONE_ENV')
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    INDEX_NAME = os.getenv('PINECONE_INDEX','ai-logs')
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(INDEX_NAME, dimension=model.get_sentence_embedding_dimension())
    idx = pinecone.Index(INDEX_NAME)
    def embed_texts(texts: List[str]):
        vecs = model.encode(texts, show_progress_bar=False)
        ids = [str(i) for i in range(len(vecs))]
        items = [(ids[i], vecs[i].tolist()) for i in range(len(vecs))]
        idx.upsert(items)
        return [v.tolist() for v in vecs]

else:
    raise RuntimeError('Unknown EMBED_PROVIDER')


