import logging
import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from models import ScreeningRequest, ScreeningResponse
from agent import screen_candidates

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PlacementOS Resume Screener",
    description="LangChain-powered resume screening agent for campus placement drives",
    version="1.0.0",
)


@app.exception_handler(Exception)
async def global_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception on %s: %s", request.url.path, exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "placement-resume-screener",
        "groq_key_set": bool(os.getenv("GROQ_API_KEY")),
    }


@app.post("/screen", response_model=ScreeningResponse)
async def screen(request: ScreeningRequest):
    if len(request.resumes) > 100:
        raise HTTPException(status_code=400, detail="Max 100 resumes per request")
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="job_description is required")

    logger.info(
        "Screening %d resumes for JD: %.60s...",
        len(request.resumes),
        request.job_description,
    )
    return await screen_candidates(request)
