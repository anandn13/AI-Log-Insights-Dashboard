from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import logs
from routers import bulk_ingest, auth as auth_router
import os

app = FastAPI(title="AI Log Insights Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api", tags=["auth"])
app.include_router(logs.router, prefix="/api/logs", tags=["logs"])
app.include_router(bulk_ingest.router, prefix="/api/logs", tags=["logs"])

@app.get("/")
def root():
    return {"status":"ok", "service":"ai-log-insights"}


