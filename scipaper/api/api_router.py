from fastapi import APIRouter
from scipaper.api.endpoints import papers, users, ingest, analysis, search, collaborators

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(papers.router, prefix="/papers", tags=["papers"])
api_router.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
api_router.include_router(analysis.router, prefix="/analyze", tags=["analysis"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(collaborators.router, prefix="/collaborators", tags=["collaborators"])
