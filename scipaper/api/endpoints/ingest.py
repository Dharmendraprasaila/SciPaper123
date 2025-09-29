from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from scipaper import crud, schemas
from scipaper.database import get_db
from scipaper.services import pubmed, arxiv, elasticsearch, neo4j

router = APIRouter()

@router.post("/", response_model=List[schemas.Paper])
async def ingest_papers(query: str, source: str, max_results: int = 10, db: Session = Depends(get_db)):
    logging.info(f"Starting ingestion for query='{query}' from source='{source}' with max_results={max_results}")
    """Ingest papers from a given source based on a query."""
    if source.lower() == "pubmed":
        article_ids = await pubmed.search_pubmed(query, max_results)
        articles = await pubmed.fetch_pubmed_articles(article_ids)
    elif source.lower() == "arxiv":
        articles = await arxiv.search_arxiv(query, max_results)
    else:
        logging.error(f"Invalid source specified: {source}")
        raise HTTPException(status_code=400, detail="Invalid source. Choose from 'pubmed' or 'arxiv'.")

    logging.info(f"Found {len(articles)} articles to ingest.")
    created_papers = []
    for article in articles:
        # Ensure authors is a list of dicts
        if 'authors' in article and isinstance(article['authors'], list) and all(isinstance(a, str) for a in article['authors']):
            article['authors'] = [{'name': author} for author in article['authors']]
        
        # Ensure all fields have valid defaults before creating the paper
        paper_data = {
            'source': article.get('source'),
            'source_id': article.get('source_id'),
            'title': article.get('title'),
            'authors': article.get('authors', []),
            'year': article.get('year'),
            'journal': article.get('journal'),
            'url': article.get('url'),
            'doi': article.get('doi'),
            'language': article.get('language'),
            'abstract': article.get('abstract')
        }
        paper_in = schemas.PaperCreate(**paper_data)
        created_paper = crud.create_paper(db=db, paper=paper_in)
        elasticsearch.index_paper(created_paper)
        neo4j_service = neo4j.get_neo4j_service()
        neo4j_service.add_paper_and_authors(created_paper)
        created_papers.append(created_paper)
    
    logging.info(f"Successfully ingested and processed {len(created_papers)} papers.")
    return created_papers
