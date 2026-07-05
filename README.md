<div align="center">

# :robot: ShortlistAI - AI Based Resume Shortlisting

### FastAPI web app that compares resumes with any job description and generates an explainable AI-style shortlisting report.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![PDF DOCX](https://img.shields.io/badge/PDF%2FDOCX-Upload-22C55E?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Resume%20Matching-8B5CF6?style=for-the-badge)

**Upload a resume. Paste a job description. Get match score, ranking, matched skills, missing skills, verdict, and improvement suggestions.**

[:rocket: Run Locally](#rocket-run-locally) | [:sparkles: Features](#sparkles-features) | [:brain: How It Works](#brain-how-it-works) | [:electric_plug: API](#electric_plug-api-endpoints) | [:file_folder: Structure](#file_folder-project-structure)

</div>

---

## :pushpin: Project Overview

**ShortlistAI** is an AI-based resume shortlisting web application built for recruiters, HR teams, students, and job seekers. It analyzes how well a candidate resume matches a specific job description and returns a clear, professional screening report.

The system supports **PDF** and **DOCX** resume uploads, extracts text from the file, compares it with the job description, detects relevant skills, calculates a weighted match score, and gives practical improvement suggestions.

> This project is designed to be portfolio-ready, interview-friendly, and easy to explain during viva/project reviews.

---

## :sparkles: Features

| Feature | Description |
| --- | --- |
| :page_facing_up: Resume Upload | Upload candidate resumes in `PDF` or `DOCX` format |
| :memo: Job Description Matching | Paste any job description for custom role-based analysis |
| :dart: Match Score | Generates a professional score out of `100` |
| :trophy: Candidate Ranking | Shows ranking tier such as strong fit, competitive, or low alignment |
| :white_check_mark: Matched Skills | Highlights skills found in both resume and job description |
| :warning: Missing Skills | Shows important job skills not clearly present in the resume |
| :bar_chart: Score Breakdown | Explains score across skills, experience, relevance, education, and quality |
| :bulb: Improvement Suggestions | Gives actionable tips to improve resume shortlisting chances |
| :brain: Optional LLM Layer | Uses Groq API when configured, with local rule-based fallback |
| :lock: Privacy Friendly | Processes uploaded files in memory and does not store resumes |
| :art: Modern UI | Attractive responsive frontend with drag-and-drop upload |

---

## :desktop_computer: Application Flow

```text
User uploads PDF/DOCX resume
          |
          v
User pastes job description
          |
          v
FastAPI receives multipart form data
          |
          v
Text is extracted from resume
          |
          v
Skills, experience, education, relevance, and quality are analyzed
          |
          v
System returns score, verdict, ranking, gaps, and suggestions
```

---

## :brain: How It Works

ShortlistAI uses a **hybrid AI-style screening approach**:

1. **Text Extraction** - Reads resume content from PDF/DOCX files.
2. **Skill Detection** - Finds technical, business, cloud, database, and professional skills.
3. **Job Relevance Analysis** - Compares resume text with job description text.
4. **Experience Matching** - Checks years of experience and seniority signals.
5. **Education Matching** - Looks for degree and qualification fit.
6. **Resume Quality Review** - Checks sections, contact info, action verbs, and measurable impact.
7. **LLM Enhancement** - If `GROQ_API_KEY` is available, the app asks an LLM for a structured recruiter-style report.
8. **Safe Fallback** - If no API key is present, the local explainable scoring engine still works.

---

## :bar_chart: Scoring Model

| Category | Weight |
| --- | ---: |
| Skills Match | `40%` |
| Experience Alignment | `20%` |
| Job Description Relevance | `20%` |
| Education Alignment | `10%` |
| Resume Quality | `10%` |

The final score is normalized from `0` to `100`, making the result easy to understand and present.

---

## :hammer_and_wrench: Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python, FastAPI, Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| Templates | Jinja2 |
| PDF Parsing | pypdf |
| DOCX Parsing | python-docx |
| AI/LLM Optional | Groq API |
| Testing | unittest, FastAPI TestClient |

---

## :file_folder: Project Structure

```text
AI Based Resume/
|
|-- app.py                  # FastAPI server, routes, validation, file upload API
|-- env_loader.py           # Loads local environment variables from .env
|-- file_parser.py          # Extracts text from PDF and DOCX resumes
|-- llm_resume_analyzer.py  # Optional Groq LLM screening layer
|-- resume_analyzer.py      # Core scoring, skill matching, verdicts, suggestions
|-- requirements.txt        # Python dependencies
|-- README.md               # Project documentation
|
|-- templates/
|   `-- index.html          # Main web page template
|
|-- static/
|   |-- css/
|   |   `-- styles.css      # Modern responsive styling
|   `-- js/
|       `-- app.js          # File upload, API call, and result rendering
|
`-- tests/
    `-- test_analyzer.py    # Analyzer and FastAPI endpoint tests
```

---

## :rocket: Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-based-resume-shortlisting.git
cd ai-based-resume-shortlisting
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Groq API - Optional

The project works without an API key using the local scoring engine. To enable LLM-assisted screening, create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
USE_GROQ_LLM=true
```

To force local-only analysis:

```env
USE_GROQ_LLM=false
```

### 6. Start the App

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

FastAPI docs are available at:

```text
http://127.0.0.1:5000/docs
```

---

## :electric_plug: API Endpoints

### Health Check

```http
GET /api/health
```

Example response:

```json
{
  "status": "ok"
}
```

### Analyze Resume

```http
POST /api/analyze
```

Form data:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `resume` | File | Yes | PDF or DOCX resume |
| `job_description` | Text | Yes | Complete job description, minimum 80 characters |

Response includes:

```json
{
  "file_name": "candidate.docx",
  "match_score": 82,
  "ranking": { "tier": "A", "label": "Strong contender" },
  "verdict": { "title": "Highly recommended" },
  "matched_skills": [],
  "missing_skills": [],
  "score_breakdown": [],
  "suggestions": []
}
```

---

## :test_tube: Run Tests

```bash
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 3 tests
OK
```

---

## :dart: Use Cases

- AI/ML mini project
- Final-year college project
- Resume screening demo for HR teams
- Job seeker resume improvement tool
- FastAPI portfolio project
- GitHub project for interviews

---

## :jigsaw: Key Learning Outcomes

This project demonstrates:

- FastAPI routing and file upload handling
- Multipart form processing
- PDF/DOCX text extraction
- Rule-based NLP and scoring logic
- Optional LLM integration
- Frontend-to-backend API communication
- Clean UI rendering with JavaScript
- Unit testing with FastAPI TestClient

---

## :crystal_ball: Future Enhancements

- Upload and rank multiple resumes at once
- Export candidate report as PDF
- Add recruiter login and saved history
- Add database support with PostgreSQL or MongoDB
- Use embeddings for deeper semantic similarity
- Add admin dashboard with analytics
- Deploy on Render, Railway, or Azure

---

## :warning: Responsible Use

ShortlistAI is a **decision-support tool**, not a replacement for human hiring judgment. It should be used to support fair and consistent screening, not to make final hiring decisions automatically.

Avoid using protected characteristics such as age, gender, religion, caste, ethnicity, disability, marital status, or nationality in screening decisions.

---

## :woman_technologist: Author

Made with :heart: for AI-based resume shortlisting projects.

If this project helps you, give it a :star: on GitHub!
