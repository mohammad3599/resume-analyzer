from pydantic import BaseModel
from typing import Optional

class ResumeRequest(BaseModel):
    resume_text: str

class ResumeResponse(BaseModel):
    score: int
    match_score: int  # درصد تطابق
    strengths: list[str]
    weaknesses: list[str]
    missing_skills: list[str]  # مهارت‌های缺失
    suggestions: list[str]
    suggested_roles: list[str]
    career_level: str  # Junior, Mid, Senior, Lead
    summary: str
    technical_skills: list[str]
    soft_skills: list[str]
    years_experience: Optional[float] = None