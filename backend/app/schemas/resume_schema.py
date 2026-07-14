from pydantic import BaseModel


class ExtractResumeRequest(BaseModel):
    filename: str