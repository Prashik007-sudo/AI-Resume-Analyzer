from pydantic import BaseModel, Field


class SectionScore(BaseModel):
    score: int
    suggestions: list[str]


class ScoreBreakdown(BaseModel):
    contact: int = Field(..., ge=0, le=10)
    skills: int = Field(..., ge=0, le=20)
    education: int = Field(..., ge=0, le=15)
    experience: int = Field(..., ge=0, le=25)
    projects: int = Field(..., ge=0, le=15)
    certifications: int = Field(..., ge=0, le=5)
    summary: int = Field(..., ge=0, le=10)


class ATSScoreResponse(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    breakdown: ScoreBreakdown
    suggestions: list[str]