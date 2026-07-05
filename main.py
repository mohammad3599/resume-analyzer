import os
import logging
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from models import ResumeRequest, ResumeResponse
from ai_service import analyze_resume
import shutil
import re

# ==============================
#  تنظیمات Logging (ثبت رویدادها)
# ==============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==============================
#  برنامه FastAPI
# ==============================
app = FastAPI(
    title="Resume Analyzer API",
    description="تحلیل هوشمند رزومه با استفاده از AI",
    version="2.0.0"
)

# ==============================
#  اندپوینت‌های GET
# ==============================

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "🚀 Resume Analyzer API is running!",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {
        "status": "healthy",
        "service": "Resume Analyzer",
        "version": "2.0.0"
    }

# ==============================
#  اندپوینت‌های POST
# ==============================

@app.post("/analyze", response_model=ResumeResponse)
def analyze(request: ResumeRequest):
    logger.info(f"Analyze request received. Text length: {len(request.resume_text)}")
    
    # اعتبارسنجی پیشرفته
    if not request.resume_text or len(request.resume_text.strip()) < 20:
        logger.warning("Invalid resume text: too short or empty")
        raise HTTPException(
            status_code=400,
            detail="متن رزومه نباید خالی باشد و باید حداقل ۲۰ کاراکتر داشته باشد."
        )
    
    try:
        result = analyze_resume(request.resume_text)
        if isinstance(result, dict):
            response = ResumeResponse(**result)
            logger.info(f"Analysis successful. Score: {response.score}")
            return response
        return result
    except Exception as e:
        logger.error(f"Error in analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطای داخلی سرور: {str(e)}")

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    logger.info(f"Upload request received: {file.filename}")
    
    # بررسی نوع فایل
    allowed_extensions = [".pdf", ".docx"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        logger.warning(f"Unsupported file type: {file_extension}")
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
        
        logger.info(f"File saved successfully: {file_path}")
        
        # ==============================
        #  استخراج متن از فایل (برای PDF و DOCX)
        # ==============================
        extracted_text = ""
        try:
            if file_extension == ".pdf":
                import PyPDF2
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        extracted_text += page.extract_text() or ""
            elif file_extension == ".docx":
                import docx
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    extracted_text += para.text + "\n"
        except ImportError:
            logger.warning("PDF/DOCX libraries not installed. Install PyPDF2 and python-docx.")
            extracted_text = "⚠️ کتابخانه‌های استخراج متن نصب نشده‌اند."
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            extracted_text = f"⚠️ خطا در استخراج متن: {str(e)}"
        
        return {
            "message": "✅ فایل با موفقیت آپلود شد",
            "filename": file.filename,
            "size": os.path.getsize(file_path),
            "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
        }
    
    except Exception as e:
        logger.error(f"Error in upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطا در آپلود فایل: {str(e)}")

# ==============================
#  هندلر خطاهای ۴۰۴
# ==============================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    logger.warning(f"404 Not Found: {request.url}")
    return JSONResponse(
        status_code=404,
        content={"detail": "مسیر مورد نظر پیدا نشد. لطفاً از مستندات استفاده کنید: /docs"}
    )

# ==============================
#  اجرا (برای دیپلوی)
# ==============================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True if os.getenv("ENV") == "development" else False
    )