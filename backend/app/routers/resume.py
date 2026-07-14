from fastapi import APIRouter, UploadFile, File

from app.services.resume_services import ResumeService

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    return await ResumeService.save_resume(file)