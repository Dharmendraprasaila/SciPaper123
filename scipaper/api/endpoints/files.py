from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import uuid

from scipaper import crud, schemas
from scipaper.database import get_db
from scipaper.tasks.analysis_tasks import analyze_pdf_task
from supabase import create_client, Client
from scipaper.config import settings

router = APIRouter()
supabase: Client = create_client(settings.supabase_url, settings.supabase_service_key)

@router.post("/{paper_id}/upload-pdf")
async def upload_pdf(paper_id: uuid.UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Uploads a PDF, saves it to Supabase Storage, and triggers an analysis task."""
    db_paper = crud.get_paper(db, paper_id=paper_id)
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    try:
        # Define a unique path for the file in storage
        file_path = f"{paper_id}/{uuid.uuid4()}.pdf"
        
        # Upload the file to Supabase Storage
        supabase.storage.from_("paper_files").upload(file_path, file.file.read())

        # Create a record in the paper_files table
        paper_file_in = schemas.PaperFileCreate(
            paper_id=paper_id,
            storage_path=file_path,
            mime=file.content_type,
            pages=0  # You could use PyPDF2 here to get the page count if needed
        )
        crud.create_paper_file(db=db, paper_file=paper_file_in)

        # Trigger the background analysis task
        analyze_pdf_task.delay(str(paper_id), file_path)

        return {"message": "File uploaded and analysis started.", "storage_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
