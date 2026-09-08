from fastapi import APIRouter

from app.schemas.jd_schema import (
    JDExtractionRequest,
    JobMatchRequest
)

from app.services.jd_service import JDService
from app.services.job_matching_service import JobMatchingService


router = APIRouter(
    prefix="/job-description",
    tags=["Job Description"]
)


@router.post("/extract")
def extract_job_description(
    request: JDExtractionRequest
):
    return JDService.extract_job_description(
        request.text
    )


@router.post("/match")
def match_job_description(
    request: JobMatchRequest
):
    return JobMatchingService.match(
        request.resume,
        request.job_description
    )