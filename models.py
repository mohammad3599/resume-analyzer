from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ResumeRequest:
    resume_text: str

@dataclass
class ResumeResponse:
    score: int
    match_score: int
    strengths: List[str]
    weaknesses: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    suggested_roles: List[str]
    career_level: str
    summary: str
    technical_skills: List[str]
    soft_skills: List[str]
    years_experience: Optional[float] = None