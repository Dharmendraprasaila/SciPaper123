from fastapi import APIRouter
from typing import List

from scipaper.services import neo4j

router = APIRouter()

@router.get("/")
def get_collaboration_suggestions_endpoint(topic: str):
    """Gets collaboration suggestions from Neo4j."""
    return neo4j.get_collaboration_suggestions(topic)
