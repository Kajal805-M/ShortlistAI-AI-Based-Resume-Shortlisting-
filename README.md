<div align="center">

# 🤖 ShortlistAI — AI Based Resume Shortlisting

### A smart, explainable resume screening web app for matching any resume with any job description.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_App-000000?style=for-the-badge&logo=flask&logoColor=white)
![PDF](https://img.shields.io/badge/PDF%2FDOCX-Upload-22C55E?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

### 🚀 [Live Demo / Local Preview](https://qv4g3xk3-5000.inc1.devtunnels.ms)

</div>

---

## 📌 Project Overview

**ShortlistAI** is an attractive AI-inspired resume shortlisting application that helps recruiters, HR teams, students, and job seekers evaluate how well a resume matches a specific job description.

Users can upload a **PDF/DOCX resume**, paste any **job description**, and instantly receive a professional analysis report with:

- Match score
- Candidate ranking tier
- Matched skills
- Missing skills
- Score breakdown
- Recruiter-style verdict
- Resume improvement suggestions

The project is designed to be **simple to run, beautiful to use, and easy to explain in college projects, interviews, and GitHub portfolios**.

---

## ✨ Key Features

| Feature | Description |
| --- | --- |
| 📄 Resume Upload | Supports resume upload in `PDF` and `DOCX` format |
| 📝 Job Description Input | Paste any job description for analysis |
| 🎯 Match Score | Generates a professional score out of `100` |
| 🏆 Ranking Tier | Shows candidate fit tier such as `Top Match`, `Strong Match`, or `Needs Improvement` |
| ✅ Matched Skills | Detects skills found in both resume and job description |
| ⚠️ Missing Skills | Highlights important skills missing from the resume |
| 📊 Score Breakdown | Explains scoring across skills, experience, education, relevance, and quality |
| 💡 Suggestions | Gives practical improvement tips for better shortlisting chances |
| 🎨 Attractive UI | Modern responsive interface with drag-and-drop upload |
| 🔒 Local Processing | Runs locally without requiring paid APIs |

---

## 🖥️ Application Preview

> Upload your resume, paste a job description, and get a clean AI-style shortlisting report instantly.

```text
Resume + Job Description
          ↓
Text Extraction
          ↓
Skill & Relevance Analysis
          ↓
Professional Match Report
```

---

## 🧠 How It Works

ShortlistAI uses an explainable rule-based AI approach instead of a black-box model. It extracts text from the uploaded resume, compares it with the job description, detects relevant skills, analyzes important resume signals, and generates a structured candidate report.

### Scoring Model

| Category | Weight |
| --- | ---: |
| Skills Match | `40%` |
| Experience Alignment | `20%` |
| Job Description Relevance | `20%` |
| Education Alignment | `10%` |
| Resume Quality | `10%` |

This makes the result easy to understand and present during demos or viva/project reviews.

---

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| PDF Parsing | pypdf |
| DOCX Parsing | python-docx |
| Testing | unittest |

---

## 📂 Project Structure

```text
AI Based Resume/
│
├── app.py                  # Flask web server and API routes
├── file_parser.py          # PDF/DOCX text extraction logic
├── resume_analyzer.py      # Resume matching and scoring engine
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── templates/
│   └── index.html          # Main web interface
│
├── static/
│   ├── css/
│   │   └── styles.css      # Attractive responsive UI styling
│   └── js/
│       └── app.js          # Upload, API call, and result rendering logic
│
└── tests/
    └── test_analyzer.py    # Unit tests for analyzer and API
```

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ai-based-resume-shortlisting.git
cd ai-based-resume-shortlisting
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv .venv
```

### 3️⃣ Activate the Virtual Environment

For Windows:

```powershell
.venv\Scripts\Activate.ps1
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

### 4️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

---

## 🧪 Run Tests

```bash
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 3 tests
OK
```

---

## 🔌 API Endpoint

### Analyze Resume

```http
POST /api/analyze
```

Form data:

| Field | Type | Required |
| --- | --- | --- |
| `resume` | PDF/DOCX file | Yes |
| `job_description` | Text | Yes |

Response includes:

- `match_score`
- `ranking`
- `verdict`
- `matched_skills`
- `missing_skills`
- `score_breakdown`
- `suggestions`

---

## 🎯 Use Cases

- College final-year project
- AI/ML mini project
- HR resume screening demo
- Job seeker resume optimization tool
- GitHub portfolio project
- Flask web development practice

---

## 🌟 Why This Project Is Useful

Recruiters often receive many resumes for one job opening. Manually reviewing every resume takes time and may miss important details. ShortlistAI helps by giving a quick, structured, and explainable first-level analysis.

For job seekers, it also works as a resume improvement assistant by showing missing skills and giving targeted suggestions.

---

## 🔮 Future Enhancements

- Add login system for recruiters
- Store candidate reports in a database
- Export analysis as PDF
- Add multiple resume ranking at once
- Integrate advanced NLP embeddings
- Add dashboard analytics for HR users
- Deploy on Render, Railway, or PythonAnywhere

---

## ⚠️ Responsible Use

ShortlistAI is a **decision-support tool**, not a final hiring authority. It should be used to assist human reviewers, not replace them. Final hiring decisions should always consider human judgment, transferable skills, accessibility needs, and fair hiring practices.

---

## 👩‍💻 Author

**Made with ❤️ for AI-based resume shortlisting projects.**

If you like this project, consider giving it a ⭐ on GitHub!
