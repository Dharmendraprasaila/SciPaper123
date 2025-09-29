from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
import uuid

from scipaper import crud, schemas
from scipaper.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Paper)
def create_paper(paper: schemas.PaperCreate, db: Session = Depends(get_db)):
    return crud.create_paper(db=db, paper=paper)

@router.get("/", response_model=List[schemas.Paper])
def read_papers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    papers = crud.get_papers(db, skip=skip, limit=limit)
    return papers

@router.get("/{paper_id}", response_model=schemas.Paper)
def read_paper(paper_id: uuid.UUID, db: Session = Depends(get_db)):
    db_paper = crud.get_paper(db, paper_id=paper_id)
    if db_paper is None:
        logging.warning(f"Paper lookup failed: Paper with id {paper_id} not found.")
        raise HTTPException(status_code=404, detail="Paper not found")
    return db_paper
