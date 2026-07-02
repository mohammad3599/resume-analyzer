from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from models import ResumeRequest, ResumeResponse
from ai_service import analyze_resume
import shutil
import os

app = FastAPI(
    title="Resume Analyzer API",
    description="تحلیل هوشمند رزومه با استفاده از AI",
    version="2.0.0"
)

# ==================== اندپوینت‌های GET ====================

@app.get("/")
def root():
    return {
        "message": "🚀 Resume Analyzer API is running!",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Resume Analyzer",
        "version": "2.0.0"
    }

# ==================== اندپوینت‌های POST ====================

@app.post("/analyze", response_model=ResumeResponse)
def analyze(request: ResumeRequest):
    # اعتبارسنجی ورودی
    if not request.resume_text or len(request.resume_text.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="متن رزومه نباید خالی باشد و باید حداقل ۲۰ کاراکتر داشته باشد."
        )
    
    try:
        result = analyze_resume(request.resume_text)
        if isinstance(result, dict):
            return ResumeResponse(**result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطای داخلی سرور: {str(e)}")

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # بررسی نوع فایل
    allowed_extensions = [".pdf", ".docx"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="فرمت فایل پشتیبانی نمی‌شود. فقط PDF و DOCX مجاز هستند."
        )
    
    try:
        # ایجاد پوشه uploads اگر وجود ندارد
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
        
        # ذخیره فایل
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # اینجا باید کد استخراج متن رو اضافه کنی
        # فعلاً یه پاسخ تستی برمی‌گردونه
        return {
            "message": "✅ فایل با موفقیت آپلود شد",
            "filename": file.filename,
            "size": os.path.getsize(file_path),
            "note": "⚠️ استخراج متن از فایل هنوز فعال نشده. برای فعال‌سازی، کتابخانه‌های PyPDF2 یا python-docx رو نصب کن."
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در آپلود فایل: {str(e)}")

# ==================== هندلر خطاهای ۴۰۴ ====================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "مسیر مورد نظر پیدا نشد. لطفاً از مستندات استفاده کنید: /docs"}
    )

# ==================== اجرا ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )