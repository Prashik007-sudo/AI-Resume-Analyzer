from fastapi import APIRouter

from app.schemas.jd_schema import JDExtractionRequest
from app.services.jd_service import JDService

router = APIRouter(
    prefix="/job-description",
    tags=["Job Description"]
)


@router.post("/extract")
def extract_job_description(request: JDExtractionRequest):

    return JDService.extract_job_description(
        request.text
    )