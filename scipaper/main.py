from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
from scipaper.api.api_router import api_router
from scipaper.logging_config import setup_logging
import logging
import time

# Call this at the very beginning
setup_logging()

app = FastAPI(title="SciPaper")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    duration = time.time() - start_time
    logging.info(f"Response: {response.status_code} (took {duration:.2f}s)")
    return response


# Get the absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

