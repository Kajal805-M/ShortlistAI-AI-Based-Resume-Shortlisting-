# ShortlistAI - AI Based Resume Shortlisting

ShortlistAI is a FastAPI web app that compares a candidate resume with a job description and returns an explainable screening report. It supports PDF and DOCX uploads, extracts resume text in memory, scores role fit, and highlights matched skills, missing skills, ranking, verdict, and improvement suggestions.

The app works locally without an API key using the built-in rule-based analyzer. If a Gemini API key is configured, it can optionally enhance the report with an LLM-assisted analysis layer.

## Features

- Upload PDF or DOCX resumes up to 8 MB.
- Paste any complete job description.
- Generate a match score out of 100.
- Show matched skills, missing skills, score breakdown, ranking, and verdict.
- Provide practical resume improvement suggestions.
- Process uploaded resumes in memory without saving files.
- Use local rule-based analysis by default, with optional Gemini LLM support.
- Includes unit tests for analyzer behavior and the API endpoint.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Jinja2
- HTML, CSS, JavaScript
- pypdf
- python-docx
- Google GenAI SDK, optional
- unittest and FastAPI TestClient

## Project Structure

```text
AI Based Resume/
|-- app.py
|-- env_loader.py
|-- file_parser.py
|-- llm_resume_analyzer.py
|-- resume_analyzer.py
|-- requirements.txt
|-- README.md
|-- templates/
|   `-- index.html
|-- static/
|   |-- css/
|   |   `-- styles.css
|   `-- js/
|       `-- app.js
`-- tests/
    `-- test_analyzer.py
```

## Run Locally

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the app:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

API docs are available at:

```text
http://127.0.0.1:5000/docs
```

## Optional Gemini Configuration

The app runs without these values. To enable LLM-assisted analysis, create a local `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.1-flash-lite
USE_GEMINI_LLM=true
```

To force local-only analysis:

```env
USE_GEMINI_LLM=false
```

## API Endpoints

Health check:

```http
GET /api/health
```

Analyze resume:

```http
POST /api/analyze
```

Required multipart form fields:

| Field | Type | Description |
| --- | --- | --- |
| `resume` | File | PDF or DOCX resume |
| `job_description` | Text | Complete job description, minimum 80 characters |

## Run Tests

```powershell
python -m unittest discover -s tests -v
```

## Responsible Use

ShortlistAI is a decision-support tool, not a final hiring decision system. Review candidates holistically and avoid using protected characteristics in screening decisions.
