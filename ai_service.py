import json

def analyze_resume(resume_text: str):
    # این یه خروجی نمونه‌ست با فیلدهای جدید
    return {
        "score": 85,
        "match_score": 78,  # درصد تطابق با شغل مورد نظر
        "strengths": ["React", "TypeScript", "Team Leadership"],
        "weaknesses": ["No cloud experience", "No mobile experience"],
        "missing_skills": ["Docker", "AWS", "CI/CD"],  # مهارت‌های کم‌داشته
        "suggestions": ["Add more quantifiable achievements", "Include GitHub link"],
        "suggested_roles": ["Senior Frontend Developer", "React Team Lead"],
        "career_level": "Senior",  # سطح شغلی
        "summary": "Experienced frontend developer with 6 years of experience and strong React skills.",
        "technical_skills": ["React", "TypeScript", "JavaScript", "CSS", "Redux"],
        "soft_skills": ["Leadership", "Communication", "Problem Solving"],
        "years_experience": 6.0
    }