import os
import fitz
import shutil
from fastapi import UploadFile, HTTPException

from app.utils.text_cleaner import TextCleaner
from app.services.resume_parser import ResumeParser

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ResumeService:

    @staticmethod
    def save_resume(file: UploadFile):

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
    
    @staticmethod
    def extract_text(file_path: str):
        document = fitz.open(file_path)

        text = ""

        for page in document:
           text += page.get_text()

        document.close()

        cleaned_text = TextCleaner.clean_text(text)

        return cleaned_text
    
    @staticmethod
    def extract_resume(filename: str):

        file_path = os.path.join(
         UPLOAD_FOLDER,
         filename
        )

        if not os.path.exists(file_path):
          raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

        text = ResumeService.extract_text(file_path)

        email = ResumeParser.extract_email(text)

        phone = ResumeParser.extract_phone(text)


        return {
        "filename": filename,
        "email": email,
        "phone": phone,
        "text": text
       }