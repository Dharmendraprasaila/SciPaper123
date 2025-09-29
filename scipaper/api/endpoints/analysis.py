from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
import time
import logging

from scipaper import crud, schemas
from scipaper.database import get_db
from scipaper.services import openai_analyzer

router = APIRouter()

@router.post("/{paper_id}", response_model=schemas.Analysis)
async def analyze_paper_endpoint(paper_id: uuid.UUID, db: Session = Depends(get_db)):
    """Triggers the analysis of a single paper by its ID."""
    db_paper = crud.get_paper(db, paper_id=paper_id)
    if db_paper is None:
        logging.error(f"Analysis failed: Paper with id {paper_id} not found.")
        raise HTTPException(status_code=404, detail="Paper not found")

    if not db_paper.abstract:
        logging.error(f"Analysis failed: Paper with id {paper_id} has no abstract.")
        raise HTTPException(status_code=400, detail="Paper has no abstract to analyze.")

    start_time = time.time()
    
    try:
        analysis_data = await openai_analyzer.analyze_paper(db_paper.title, db_paper.abstract)
    except Exception as e:
        logging.error(f"OpenAI analysis failed for paper {paper_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze paper with OpenAI: {e}")

    duration_ms = int((time.time() - start_time) * 1000)

    analysis_in = schemas.AnalysisCreate(
        paper_id=paper_id,
        status="completed",
        duration_ms=duration_ms,
        **analysis_data
    )

    created_analysis = crud.create_analysis(db=db, analysis=analysis_in)
    return created_analysis
