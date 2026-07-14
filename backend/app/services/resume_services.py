import os
import shutil
from fastapi import UploadFile, HTTPException

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ResumeService:

    @staticmethod
    async def save_resume(file: UploadFile):

        if not file.filename.endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        return {
            "filename": file.filename,
            "path": file_path,
            "message": "Resume uploaded successfully."
        }