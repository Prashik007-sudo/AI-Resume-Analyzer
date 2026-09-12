from typing import List
from pydantic import BaseModel, Field


class MatchResponse(BaseModel):
    overall_match: int

    required_skill_match: int
    preferred_skill_match: int
    education_match: bool
    experience_match: bool
    keyword_match: int

    matched_required_skills: List[str] = Field(default_factory=list)
    related_required_skills: List[str] = Field(default_factory=list)
    missing_required_skills: List[str] = Field(default_factory=list)

    matched_preferred_skills: List[str] = Field(default_factory=list)
    related_preferred_skills: List[str] = Field(default_factory=list)
    missing_preferred_skills: List[str] = Field(default_factory=list)

    overall_semantic_match: int
    experience_relevance: int
    project_relevance: int
    skill_relevance: int
    responsibility_alignment: int

    reasoning: str
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)

    suggestions: List[str] = Field(default_factory=list)