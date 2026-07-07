import os
import logging
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from models import ResumeRequest, ResumeResponse
from ai_service import analyze_resume
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================
#  برنامه FastAPI با docs_url فعال
# ==============================
app = FastAPI(
    title="Resume Analyzer API",
    description="تحلیل هوشمند رزومه با استفاده از AI",
    version="2.0.0",
    docs_url="/docs",        # ← این خط رو حتماً داشته باش
    redoc_url="/redoc"       # ← این خط رو هم داشته باش (اختیاری)
)

# ==============================
#  اندپوینت‌ها
# ==============================

@app.get("/")
def root():
    return {
        "message": "🚀 Resume Analyzer API is running!",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Resume Analyzer"}

@app.post("/analyze")
def analyze(request: ResumeRequest):
    if not request.resume_text or len(request.resume_text.strip()) < 20:
        raise HTTPException(status_code=400, detail="متن رزومه نباید خالی باشد و باید حداقل ۲۰ کاراکتر داشته باشد.")
    
    try:
        result = analyze_resume(request.resume_text)
        return ResumeResponse(**result)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطای داخلی سرور: {str(e)}")

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": "✅ فایل با موفقیت آپلود شد", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)