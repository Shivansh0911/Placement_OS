from pydantic import BaseModel, Field, field_validator
from typing import List, Literal


class ResumeInput(BaseModel):
    student_id: str
    name: str
    resume_text: str

    @field_validator("resume_text")
    @classmethod
    def resume_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("resume_text cannot be blank")
        return v.strip()


class ScreeningRequest(BaseModel):
    job_description: str
    eligibility_criteria: dict = Field(
        default_factory=lambda: {"min_cgpa": 6.0, "branches": [], "max_backlogs": 0}
    )
    resumes: List[ResumeInput]

    @field_validator("resumes")
    @classmethod
    def at_least_one(cls, v: list) -> list:
        if not v:
            raise ValueError("resumes list cannot be empty")
        return v


Recommendation = Literal["STRONG_YES", "YES", "MAYBE", "NO"]


class CandidateScore(BaseModel):
    student_id: str
    name: str
    score: float = Field(ge=0, le=100)
    reasoning: str
    strengths: List[str]
    gaps: List[str]
    recommendation: Recommendation


class ScreeningResponse(BaseModel):
    ranked_candidates: List[CandidateScore]
    screening_summary: str
    total_screened: int
    recommended_count: int
