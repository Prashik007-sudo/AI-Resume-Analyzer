from typing import List
from pydantic import BaseModel, Field


class Education(BaseModel):
    degree: str
    institution: str
    year: str
    percentage: str


class Experience(BaseModel):
    company: str
    designation: str
    duration: str
    description: str


class Project(BaseModel):
    name: str
    role: str
    duration: str
    development_environment: str
    testing_environment: str
    description: str


class ExtractResumeRequest(BaseModel):
    filename: str


class ResumeResponse(BaseModel):
    filename: str

    email: str | None = None
    phone: str | None = None
    name: str | None = None

    skills: List[str] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)

    projects: List[Project] = Field(default_factory=list)

    certifications: List[str] = Field(default_factory=list)

    summary: str | None = None