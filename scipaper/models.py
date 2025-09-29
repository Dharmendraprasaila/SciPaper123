from sqlalchemy import create_engine, Column, String, Integer, JSON, DateTime, Date, ARRAY, Uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    name = Column(String)
    affiliation = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    source = Column(String)
    source_id = Column(String)
    title = Column(String)
    authors = Column(JSON)
    year = Column(Integer)
    journal = Column(String)
    url = Column(String)
    doi = Column(String)
    language = Column(String)
    abstract = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PaperFile(Base):
    __tablename__ = 'paper_files'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    paper_id = Column(Uuid)
    storage_path = Column(String)
    mime = Column(String)
    pages = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Analysis(Base):
    __tablename__ = 'analyses'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    paper_id = Column(Uuid)
    status = Column(String)
    duration_ms = Column(Integer)
    findings = Column(JSON)
    methods = Column(JSON)
    datasets = Column(JSON)
    gaps = Column(JSON)
    limitations = Column(JSON)
    plagiarism = Column(JSON)
    citations = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Domain(Base):
    __tablename__ = 'domains'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)

class DomainTrend(Base):
    __tablename__ = 'domain_trends'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    domain_id = Column(Uuid)
    status = Column(String)
    duration_ms = Column(Integer)
    trends = Column(JSON)
    top_papers = Column(JSON)
    funding = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    kind = Column(String)
    payload = Column(JSON)
    status = Column(String)
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
    error = Column(String)

class Grant(Base):
    __tablename__ = 'grants'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    source = Column(String)
    call_id = Column(String)
    title = Column(String)
    deadline = Column(Date)
    url = Column(String)
    agency = Column(String)
    tags = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Proposal(Base):
    __tablename__ = 'proposals'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid)
    domain = Column(String)
    content = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
