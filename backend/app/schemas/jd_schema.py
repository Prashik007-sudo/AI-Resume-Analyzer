from typing import List

from pydantic import BaseModel, Field

from app.schemas.resume_schema import ResumeResponse


class JDResponse(BaseModel):

    raw_text: str

    job_title: str | None = None

    company: str | None = None

    location: str | None = None

    employment_type: str | None = None

    experience_required: str | None = None

    education_required: str | None = None

    required_skills: List[str] = Field(default_factory=list)

    preferred_skills: List[str] = Field(default_factory=list)

    responsibilities: List[str] = Field(default_factory=list)

    qualifications: List[str] = Field(default_factory=list)

    keywords: List[str] = Field(default_factory=list)


class JobMatchRequest(BaseModel):

    resume: ResumeResponse

    job_description: JDResponse

JobMatchRequest.model_rebuild()    


class JDExtractionRequest(BaseModel):

    text: str