import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("SUPABASE_DB_URL")

if not DB_URL:
    raise ValueError("SUPABASE_DB_URL is not set in the .env file")

# SQL statements to create tables
CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text UNIQUE,
    name text,
    affiliation text,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS papers (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source text,
    source_id text,
    title text,
    authors jsonb,
    year int,
    journal text,
    url text,
    doi text,
    language text,
    abstract text,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS paper_files (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    paper_id uuid REFERENCES papers(id) ON DELETE CASCADE,
    storage_path text,
    mime text,
    pages int,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS analyses (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    paper_id uuid REFERENCES papers(id) ON DELETE CASCADE,
    status text,
    duration_ms int,
    findings jsonb,
    methods jsonb,
    datasets jsonb,
    gaps jsonb,
    limitations jsonb,
    plagiarism jsonb,
    citations jsonb,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS domains (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text UNIQUE
);

CREATE TABLE IF NOT EXISTS domain_trends (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    domain_id uuid REFERENCES domains(id) ON DELETE CASCADE,
    status text,
    duration_ms int,
    trends jsonb,
    top_papers jsonb,
    funding jsonb,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS jobs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    kind text,
    payload jsonb,
    status text,
    started_at timestamptz,
    finished_at timestamptz,
    error text
);

CREATE TABLE IF NOT EXISTS grants (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source text,
    call_id text,
    title text,
    deadline date,
    url text,
    agency text,
    tags text[],
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS proposals (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES users(id) ON DELETE SET NULL,
    domain text,
    content jsonb,
    created_at timestamptz DEFAULT now()
);
"""

def setup_database():
    """Connects to the database and creates the tables."""
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLES_SQL)
                conn.commit()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    setup_database()
