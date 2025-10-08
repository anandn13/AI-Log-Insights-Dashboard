# 🚀 AI Log Insights Dashboard

Production-ready, end-to-end system to ingest logs, index/search in Elasticsearch, run LLM-based analysis and summaries via LangChain, and explore insights in a Streamlit dashboard.

## ✨ Features

- 📨 Ingest logs via REST or file upload
- 🔎 Index logs into Elasticsearch with structured fields
- 🧠 Semantic search via embeddings (OpenAI or local SentenceTransformers)
- 🕵️ Summaries, anomaly/error detection via LangChain chains
- 🖥️ Streamlit dashboard for exploration, QA and reports
- 🧪 CI (GitHub Actions), unit tests, Dockerized deployment

## 🧰 Tech stack

- Python 3.10+
- FastAPI, Uvicorn
- LangChain
- Elasticsearch Python client
- SentenceTransformers (local embeddings fallback)
- Streamlit
- Docker / docker-compose
- pytest

## 📦 Project layout

```
ai-log-insights/
├─ README.md
├─ LICENSE
├─ requirements.txt
├─ docker-compose.yml
├─ docker-compose.prod.yml
├─ .env.example
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ routers/
│  │  │  ├─ logs.py
│  │  │  ├─ bulk_ingest.py
│  │  │  └─ auth.py
│  │  ├─ services/
│  │  │  ├─ elasticsearch_client.py
│  │  │  ├─ embeddings.py
│  │  │  ├─ embeddings_switch.py
│  │  │  ├─ langchain_agent.py
│  │  │  ├─ langchain_chains.py
│  │  │  └─ auth.py
│  │  ├─ models/schemas.py
│  │  ├─ utils/logger.py
│  │  └─ worker/scheduler.py
│  └─ Dockerfile
├─ streamlit_app/
│  ├─ app.py
│  ├─ components/ui.py
│  └─ Dockerfile
├─ scripts/
│  ├─ generate_sample_logs.py
│  └─ ingest_sample.sh
├─ tests/
│  ├─ test_elasticsearch.py
│  └─ test_api.py
├─ .github/
│  ├─ workflows/ci.yml
│  ├─ ISSUE_TEMPLATE/
│  │  ├─ bug_report.md
│  │  └─ feature_request.md
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ FUNDING.yml
├─ docs/
│  ├─ production-deploy.md
│  └─ auth-design.md
├─ kibana/
│  ├─ dashboards/logs_saved_objects.json
│  └─ import_dashboards.sh
├─ SUPPORT.md
├─ CONTRIBUTING.md
├─ CODE_OF_CONDUCT.md
├─ SECURITY.md
├─ .flake8
├─ .pre-commit-config.yaml
├─ .dockerignore
├─ .editorconfig
└─ Makefile
```

## ⚡ Quickstart (Docker)

1. Copy `.env.example` to `.env` and set values (set `USE_LOCAL_EMBEDDINGS=true` to avoid OpenAI).
2. Start services:

```bash
docker compose up --build
```

3. Open:
- Backend API: `http://localhost:8000`
- Streamlit: `http://localhost:8501`
- Elasticsearch: `http://localhost:9200`

4. Seed sample data:

```bash
make ingest
```

5. Try a semantic search:

```bash
curl "http://localhost:8000/api/logs/search?q=timeout&k=3"
```

## 🛠️ Development (no Docker)

```bash
python -m venv .venv
. .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

Streamlit:

```bash
cd streamlit_app
export BACKEND_URL=http://localhost:8000  # on Windows: set BACKEND_URL=http://localhost:8000
streamlit run app.py --server.port 8501
```

## ✅ Tests

```bash
pytest -q
```

## ⚙️ Environment variables

You can set these in `.env`:

- ELASTIC_HOST, ELASTIC_PORT, ELASTIC_INDEX (default: `logs`)
- USE_LOCAL_EMBEDDINGS (`true`|`false`)
- LOCAL_EMBEDDINGS_MODEL (default: `all-MiniLM-L6-v2`)
- OPENAI_API_KEY (when using OpenAI)
- EMBED_PROVIDER (`local`|`openai`|`pinecone`)
- PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX
- BACKEND_HOST, BACKEND_PORT
- STREAMLIT_PORT, BACKEND_URL (Streamlit to backend)
- JWT_SECRET, AUTH_DB_PATH

## 📡 API reference (selected)

- GET `/` → service health
- POST `/api/logs/ingest` → ingest single log
- POST `/api/logs/analyze` → analyze a batch (LLM)
- GET `/api/logs/search?q=...&k=5` → semantic search
- POST `/api/auth/signup` → create user
- POST `/api/auth/token` → OAuth2 password → `access_token`
- POST `/api/logs/bulk` (Bearer token) → bulk ingest

Examples:

```bash
# single ingest
curl -X POST http://localhost:8000/api/logs/ingest \
  -H 'Content-Type: application/json' \
  -d '{"timestamp":"2025-10-08T12:00:00Z","level":"ERROR","source":"api","message":"timeout calling db"}'

# get token
curl -X POST http://localhost:8000/api/auth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=alice&password=secret'

# bulk ingest (replace TOKEN)
curl -X POST http://localhost:8000/api/logs/bulk \
  -H 'Authorization: Bearer TOKEN' -H 'Content-Type: application/json' \
  -d '[{"level":"INFO","message":"hello"},{"level":"ERROR","message":"failed"}]'
```

## 🔌 Embedding providers

- `local` (default): SentenceTransformers, fast and free. Ensure ES mapping `dims` matches the model (384 for MiniLM).
- `openai`: set `OPENAI_API_KEY`. Cost applies.
- `pinecone`: vectors are also upserted to Pinecone; keep ES mapping consistent for local similarity too.

Switch provider via `EMBED_PROVIDER`.

## ⏰ Scheduler (daily summary)

Background scheduler is available in `backend/app/worker/scheduler.py`.
To enable in the API process, add:

```python
# in backend/app/main.py
from worker.scheduler import start_scheduler
if os.getenv('ENABLE_SCHEDULER','false').lower() in ('true','1'):
    start_scheduler()
```

Then set `ENABLE_SCHEDULER=true` in `.env`.

## 🧩 Troubleshooting

- ❌ `docker compose` not found
  - Install Docker Desktop and ensure `docker` works in your shell.
- ⏳ Elasticsearch not ready / connection refused
  - First boot can take 30–60s. Retry once healthy: `curl http://localhost:9200`.
- 📏 Vector dims mismatch
  - Ensure ES index mapping `embedding.dims` matches your model dimension.
- 🔑 OpenAI errors (401/429)
  - Check `OPENAI_API_KEY`, rate limits, and consider `USE_LOCAL_EMBEDDINGS=true`.
- 🛡️ Auth errors (401)
  - Obtain token via `/api/auth/token` and use `Authorization: Bearer <token>`.

## ❓ FAQ

- Can I use Elastic Cloud? → Yes. Set `ELASTIC_HOST`, `ELASTIC_PORT`, and credentials.
- How big can logs be? → This starter is for demos; for production, add batching and backpressure (see bulk endpoint).
- How do I change the model? → Set `LOCAL_EMBEDDINGS_MODEL` and update ES dims.

## ⚙️ Performance tips

- Use `/api/logs/bulk` with batches of 500–1000 documents.
- Disable Streamlit in ingest-only environments.
- Scale backend replicas behind Traefik in `docker-compose.prod.yml`.

## 🔐 Security

See `SECURITY.md`. Report privately to `anandhabagavathileos@gmail.com`.

## 💬 Support

See `SUPPORT.md` or email `anandhabagavathileos@gmail.com`.

## 🤝 Contributing

See `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`. PRs welcome!

## 📜 License

MIT © T Anandha Bagavathi


