from fastapi import APIRouter, UploadFile, File

from app.services.resume_services import ResumeService

from app.schemas.resume_schema import ExtractResumeRequest

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
def upload_resume(file: UploadFile = File(...)):
    return  ResumeService.save_resume(file)

@router.post("/extract")
def extract_resume(request: ExtractResumeRequest):

    return ResumeService.extract_resume(
        request.filename
    )