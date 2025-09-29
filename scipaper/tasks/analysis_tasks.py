from scipaper.celery_worker import celery_app
from scipaper.services import openai_analyzer
from scipaper import crud, schemas
from scipaper.database import SessionLocal
from supabase import create_client, Client
from scipaper.config import settings
import PyPDF2
import io

# Initialize Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_service_key)

@celery_app.task
def analyze_pdf_task(paper_id: str, storage_path: str):
    """A Celery task to download, parse, and analyze a PDF from Supabase Storage."""
    db = SessionLocal()
    try:
        # 1. Download the PDF from Supabase Storage
        response = supabase.storage.from_("paper_files").download(storage_path)
        pdf_content = response

        # 2. Parse the full text of the PDF
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()

        # 3. Send the text to OpenAI for analysis
        # (We'll use the existing analyzer which works on abstracts, but for a real
        # implementation, you might create a new, more detailed prompt)
        db_paper = crud.get_paper(db, paper_id=paper_id)
        if not db_paper:
            raise Exception(f"Paper with id {paper_id} not found.")

        analysis_data = openai_analyzer.analyze_paper(db_paper.title, full_text)

        # 4. Save the results to the database
        analysis_in = schemas.AnalysisCreate(
            paper_id=paper_id,
            status="completed_full_text",
            duration_ms=0, # You could calculate this for more detailed logging
            **analysis_data
        )
        crud.create_analysis(db=db, analysis=analysis_in)

    finally:
        db.close()

    return {"status": "success", "paper_id": paper_id}
