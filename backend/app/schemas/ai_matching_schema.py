from pydantic import BaseModel, Field


class AISemanticMatch(BaseModel):
    experience_relevance: int = Field(ge=0, le=100)
    project_relevance: int = Field(ge=0, le=100)
    skill_relevance: int = Field(ge=0, le=100)
    responsibility_alignment: int = Field(ge=0, le=100)
    overall_semantic_match: int = Field(ge=0, le=100)
    reasoning: str
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)