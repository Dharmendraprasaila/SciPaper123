from sqlalchemy.orm import Session
from . import models, schemas
import uuid

# User CRUD operations
def get_user(db: Session, user_id: uuid.UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name, affiliation=user.affiliation)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Paper CRUD operations
def get_paper(db: Session, paper_id: uuid.UUID):
    return db.query(models.Paper).filter(models.Paper.id == paper_id).first()

def get_papers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paper).offset(skip).limit(limit).all()

def create_paper(db: Session, paper: schemas.PaperCreate):
    db_paper = models.Paper(**paper.dict())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

# Analysis CRUD operations
def create_analysis(db: Session, analysis: schemas.AnalysisCreate):
    db_analysis = models.Analysis(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

# Grant CRUD operations
def get_grants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Grant).offset(skip).limit(limit).all()

# Proposal CRUD operations
def create_proposal(db: Session, proposal: schemas.ProposalCreate):
    db_proposal = models.Proposal(**proposal.dict())
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal
