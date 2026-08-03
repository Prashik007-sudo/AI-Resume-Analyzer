from fastapi import APIRouter, UploadFile, File

from app.services.resume_services import ResumeService

from app.schemas.resume_schema import (
    ExtractResumeRequest,
    ResumeResponse,
)

from app.schemas.ats_schema import ATSScoreResponse
from app.services.ats_score_service import ATSScoreService

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
def upload_resume(file: UploadFile = File(...)):
    return  ResumeService.save_resume(file)

@router.post(
    "/extract",
    response_model=ResumeResponse
)
def extract_resume(request: ExtractResumeRequest):
    
    return ResumeService.extract_resume(
        request.filename
    )


@router.post(
    "/score",
    response_model=ATSScoreResponse
)
def score_resume(
    resume: ResumeResponse
):

    return ATSScoreService.calculate_score(
        resume
    )