from elasticsearch import Elasticsearch
from scipaper.config import settings
from scipaper.schemas import Paper

INDEX_NAME = "scipaper-papers"

client = Elasticsearch(
    hosts=[settings.elasticsearch_url],
    api_key=settings.elasticsearch_api_key
)

def create_index_if_not_exists():
    """Creates the 'scipaper-papers' index if it doesn't already exist."""
    if not client.indices.exists(index=INDEX_NAME):
        client.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "abstract": {"type": "text"},
                        "authors": {"type": "nested", "properties": {"name": {"type": "text"}}},
                        "journal": {"type": "keyword"},
                        "year": {"type": "integer"},
                        "doi": {"type": "keyword"},
                        "url": {"type": "keyword"},
                        "language": {"type": "keyword"}
                    }
                }
            }
        )
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

def index_paper(paper: Paper):
    """Indexes a single paper document in Elasticsearch."""
    doc = {
        "title": paper.title,
        "abstract": paper.abstract,
        "authors": paper.authors,
        "journal": paper.journal,
        "year": paper.year,
        "doi": paper.doi,
        "url": paper.url,
        "language": paper.language
    }
    client.index(index=INDEX_NAME, id=str(paper.id), document=doc)

def search_papers(query: str):
    """Searches for papers in Elasticsearch."""
    response = client.search(
        index=INDEX_NAME,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "abstract"]
                }
            }
        }
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]
