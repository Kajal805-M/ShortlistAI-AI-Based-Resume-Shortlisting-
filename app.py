import logging
import os
import time
from uuid import uuid4

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from env_loader import load_env_file
from file_parser import DocumentParseError, extract_text
from llm_resume_analyzer import analyze_resume_with_llm


load_env_file()

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("shortlistai")

app = FastAPI(title="ShortlistAI", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
MAX_FILE_SIZE = 8 * 1024 * 1024
UPLOAD_EXTENSIONS = {".pdf", ".docx"}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = uuid4().hex[:8]
    request.state.request_id = request_id
    started_at = time.perf_counter()

    if not request.url.path.startswith("/static"):
        logger.info("[%s] -> %s %s", request_id, request.method, request.url.path)

    try:
        response = await call_next(request)
    except Exception:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.exception("[%s] !! Unhandled error after %.1fms", request_id, elapsed_ms)
        raise

    elapsed_ms = (time.perf_counter() - started_at) * 1000
    if request.url.path.startswith("/static"):
        logger.debug("[%s] <- %s %s %.1fms", request_id, response.status_code, request.url.path, elapsed_ms)
    else:
        logger.info("[%s] <- %s %s %.1fms", request_id, response.status_code, request.url.path, elapsed_ms)
    return response


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.info("[%s] Rendering analyzer page", request.state.request_id)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health")
async def health(request: Request):
    logger.info("[%s] Health check OK", request.state.request_id)
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze(
    request: Request,
    resume: UploadFile | None = File(default=None),
    job_description: str = Form(default=""),
):
    request_id = request.state.request_id
    logger.info("[%s] Step 1/6: Received analysis request", request_id)

    job_description = job_description.strip()
    if not resume or not resume.filename:
        logger.warning("[%s] Validation failed: resume file is missing", request_id)
        return JSONResponse({"error": "Please upload a PDF or DOCX resume."}, status_code=400)
    if len(job_description) < 80:
        logger.warning(
            "[%s] Validation failed: job description too short (%s chars)",
            request_id,
            len(job_description),
        )
        return JSONResponse({"error": "Please paste a more complete job description (at least 80 characters)."}, status_code=400)

    extension = os.path.splitext(resume.filename.lower())[1]
    if extension not in UPLOAD_EXTENSIONS:
        logger.warning("[%s] Validation failed: unsupported file type %s", request_id, extension or "<none>")
        return JSONResponse({"error": "Unsupported file type. Please upload a PDF or DOCX file."}, status_code=400)

    try:
        logger.info(
            "[%s] Step 2/6: Validated inputs filename=%r extension=%s job_chars=%s",
            request_id,
            resume.filename,
            extension,
            len(job_description),
        )

        logger.info("[%s] Step 3/6: Reading uploaded resume bytes", request_id)
        content = await resume.read()
        logger.info("[%s] Read %.2f MB from uploaded resume", request_id, len(content) / 1024 / 1024)
        if len(content) > MAX_FILE_SIZE:
            logger.warning("[%s] Validation failed: file too large %.2f MB", request_id, len(content) / 1024 / 1024)
            return JSONResponse({"error": "The file is too large. Maximum upload size is 8 MB."}, status_code=413)

        logger.info("[%s] Step 4/6: Extracting resume text", request_id)
        resume_text = extract_text(_MemoryUpload(content), extension)
        logger.info("[%s] Extracted %s characters of resume text", request_id, len(resume_text.strip()))
        if len(resume_text.strip()) < 80:
            logger.warning("[%s] Parsing produced too little text for reliable analysis", request_id)
            return JSONResponse({"error": "Very little text could be read from this resume. Try a text-based PDF or DOCX file."}, status_code=422)

        logger.info("[%s] Step 5/6: Running resume analysis", request_id)
        report = analyze_resume_with_llm(resume_text, job_description, resume.filename)
        logger.info(
            "[%s] Step 6/6: Completed analysis mode=%s score=%s matched=%s missing=%s",
            request_id,
            report.get("analysis_mode", "unknown"),
            report.get("match_score"),
            len(report.get("matched_skills", [])),
            len(report.get("missing_skills", [])),
        )
        return report
    except DocumentParseError as error:
        logger.warning("[%s] Document parsing failed: %s", request_id, error)
        return JSONResponse({"error": str(error)}, status_code=422)
    except Exception:
        logger.exception("[%s] Resume analysis failed unexpectedly", request_id)
        return JSONResponse({"error": "We could not analyze this resume. Please try another file."}, status_code=500)


class _MemoryUpload:
    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
