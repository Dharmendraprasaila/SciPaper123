from fastapi import APIRouter
from typing import List

from scipaper.services import elasticsearch

router = APIRouter()

@router.get("/")
def search_papers_endpoint(query: str):
    """Searches for papers in Elasticsearch."""
    return elasticsearch.search_papers(query)
