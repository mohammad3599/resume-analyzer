# 🚀 Resume Analyzer API

An intelligent API for analyzing resumes (text and PDF/DOCX files) using FastAPI and Groq.

## ✨ Features
- Analyze text resumes (Persian & English)
- Upload PDF and DOCX files
- Match score calculation (`match_score`)
- Identify missing skills (`missing_skills`)
- Career level detection (`career_level`)
- Full Swagger documentation
- Input validation

## 🛠️ Tech Stack
- **FastAPI** for API development
- **Groq** for AI analysis (can be replaced with Hugging Face)
- **Pydantic** for data validation
- **Uvicorn** for server execution
- **Python-Multipart** for file uploads

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer