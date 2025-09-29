from fastapi import APIRouter
from typing import List

from scipaper.services import neo4j

router = APIRouter()

@router.get("/")
def get_collaboration_suggestions_endpoint(topic: str):
    """Gets collaboration suggestions from Neo4j."""
    neo4j_service = neo4j.get_neo4j_service()
    return neo4j_service.get_collaboration_suggestions(topic)
