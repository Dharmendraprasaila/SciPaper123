from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime, date

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    affiliation: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True

class PaperBase(BaseModel):
    source: str
    source_id: str
    title: str
    authors: Optional[List[dict]] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    language: Optional[str] = None
    abstract: Optional[str] = None

class PaperCreate(PaperBase):
    pass

class Paper(PaperBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True

class AnalysisBase(BaseModel):
    paper_id: uuid.UUID
    status: str
    duration_ms: Optional[int] = None
    findings: Optional[dict] = None
    methods: Optional[dict] = None
    datasets: Optional[dict] = None
    gaps: Optional[dict] = None
    limitations: Optional[dict] = None
    plagiarism: Optional[dict] = None
    citations: Optional[dict] = None

class AnalysisCreate(AnalysisBase):
    pass

class Analysis(AnalysisBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True

class GrantBase(BaseModel):
    source: str
    call_id: str
    title: str
    deadline: Optional[date] = None
    url: Optional[str] = None
    agency: Optional[str] = None
    tags: Optional[List[str]] = None

class GrantCreate(GrantBase):
    pass

class Grant(GrantBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True

class ProposalBase(BaseModel):
    user_id: uuid.UUID
    domain: str
    content: dict

class ProposalCreate(ProposalBase):
    pass

class Proposal(ProposalBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True
