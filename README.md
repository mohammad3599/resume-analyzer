# 🤖 Resume Analyzer API

An intelligent API for analyzing resumes (text and PDF/DOCX files) using **FastAPI** and **Groq**.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green)](https://fastapi.tiangolo.com)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---

## ✨ Features

- ✅ Analyze text resumes (Persian & English)
- ✅ Upload PDF and DOCX files
- ✅ Match score calculation (`match_score`)
- ✅ Identify missing skills (`missing_skills`)
- ✅ Career level detection (`career_level`)
- ✅ Full Swagger documentation
- ✅ Input validation
- ✅ Logging system

---

## 🛠️ Tech Stack

- **FastAPI** – API framework
- **Groq** – AI inference (can be replaced with Hugging Face)
- **Pydantic** – Data validation
- **Uvicorn** – ASGI server
- **Python-Multipart** – File uploads

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/mohammad3599/resume-analyzer.git
cd resume-analyzer