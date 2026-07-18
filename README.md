<div align="center">

# 🚀 ShortlistAI – AI-Based Resume Shortlisting 

### Intelligent Resume Screening & Job Matching using Large Language Models (LLMs)

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python"/>

<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" width="60"/>
  
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg" width="60"/>
  
<img src="https://img.shields.io/badge/AI-LLM%20Powered-success?style=for-the-badge"/>

<img src="https://img.shields.io/badge/NLP-Resume%20Analysis-orange?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Open%20Source-GitHub-black?style=for-the-badge&logo=github"/>

</p>

### 🤖 Analyze • Compare • Improve • Get Shortlisted

> **ShortlistAI** is an AI-powered resume analysis platform that intelligently compares a resume with a job description, evaluates candidate-job alignment, and provides actionable AI-generated feedback to improve interview readiness.

<p align="center">
  <a href="https://shortlistai-ai-based-resume-shortlisting.onrender.com">
    <img src="https://img.shields.io/badge/🚀%20LIVE%20DEMO-Try%20it%20Now-brightgreen?style=for-the-badge&logo=render&logoColor=white" alt="Live Demo"/>
  </a>
</p>

<p align="center">
  <b>🌐 Live App:</b> <a href="https://shortlistai-ai-based-resume-shortlisting.onrender.com">shortlistai-ai-based-resume-shortlisting.onrender.com</a>
</p>

---

⭐ **If you find this project useful, don't forget to Star the repository!**

</div>

---

## 🔗 Live Demo

Experience ShortlistAI live — no installation required:

### 👉 **[Launch ShortlistAI](https://shortlistai-ai-based-resume-shortlisting.onrender.com)**

> ⚠️ **Note:** The app is hosted on Render's free tier, so it may take **30–60 seconds** to spin up if it has been inactive. Please be patient on first load!

---

# 📖 About the Project

Recruiters spend only a few seconds scanning each resume, making it difficult for candidates to know whether their resume truly matches a job description.

**ShortlistAI** addresses this challenge by leveraging **Large Language Models (LLMs)** to analyze resumes in context rather than relying solely on keyword matching.

The system evaluates:

- Technical Skills
- Professional Experience
- Projects
- Education
- Resume Structure
- Job Relevance
- Missing Skills
- AI Recommendations

and generates intelligent feedback to help candidates improve their resumes before applying.

---
## 💻 Tech Stack

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<img src="https://img.shields.io/badge/LLM-AI-green?style=for-the-badge"/>

<img src="https://img.shields.io/badge/NLP-Prompt%20Engineering-orange?style=for-the-badge"/>

<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>

<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>

<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>

<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white"/>

<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github"/>

<img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"/>

<img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white"/>

</p>
---
# ✨ Features

### 📄 Resume Upload

- Upload Resume in **PDF**
- Upload Resume in **DOCX**

---

### 💼 Job Description Analysis

- Paste any Job Description
- AI understands role requirements
- Context-aware evaluation

---

### 🤖 LLM Powered Analysis

- Intelligent Resume Understanding
- Semantic Job Matching
- Skill Gap Detection
- Resume Strength Analysis

---

### 📊 AI Insights

- Resume Match Score
- Matched Skills
- Missing Skills
- Resume Improvement Suggestions

---

### 🎨 Beautiful Interface

- Interactive Streamlit Dashboard
- Responsive Layout
- Clean UI
- Modern Design

---

# 🧠 How It Works

```text
                 Resume Upload
                       │
                       ▼
            Resume Text Extraction
                       │
                       ▼
              Document Preprocessing
                       │
                       ▼
           Job Description Processing
                       │
                       ▼
          Large Language Model (LLM)
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
 Resume Analysis   Skill Matching   AI Suggestions
       │               │               │
       └───────────────┼───────────────┘
                       ▼
             Resume Match Evaluation
                       │
                       ▼
               Final AI Report
```

---

# 🏗 Project Architecture

```text
                    User
                      │
                      ▼
             Streamlit Web App
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    File Parser             Job Description
          │                       │
          ▼                       ▼
     Resume Text          Cleaned Job Text
                  │
                  ▼
       LLM Resume Analyzer
                  │
                  ▼
        AI Evaluation Engine
                  │
                  ▼
      Match Score & Suggestions
                  │
                  ▼
         Interactive Dashboard
```

---

# 📂 Project Structure

```text
ShortlistAI
│
├── app.py                     # Streamlit Application
├── llm_resume_analyzer.py     # LLM-based Resume Analysis
├── resume_analyzer.py         # Resume Scoring Logic
├── file_parser.py             # PDF & DOCX Parser
├── env_loader.py              # Environment Configuration
├── requirements.txt
├── README.md
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   └── index.html
│
└── tests/
    └── test_analyzer.py
```

---

# 🛠 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Programming Language | Python |
| Frontend | Streamlit |
| Artificial Intelligence | Large Language Model (LLM) |
| NLP | Prompt Engineering |
| File Parsing | PyPDF, python-docx |
| Styling | HTML, CSS, JavaScript |
| Environment | Python Virtual Environment |
| Deployment | Render |

---

# ⚙ Installation

## 🌐 Option 1: Try the Live Demo (Recommended)

No setup needed — just click and go:

### 👉 **[https://shortlistai-ai-based-resume-shortlisting.onrender.com](https://shortlistai-ai-based-resume-shortlisting.onrender.com)**

---

## 💻 Option 2: Run Locally

### Clone Repository

```bash
git clone https://github.com/Kajal805-M/ShortlistAI-AI-Based-Resume-Shortlisting-.git
```

---

### Move into Project

```bash
cd ShortlistAI-AI-Based-Resume-Shortlisting-
```

---

### Create Virtual Environment

```bash
python -m venv .venv
```

---

### Activate Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

---

### Install Requirements

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file and add your API key (if your project requires one):

```env
API_KEY=YOUR_API_KEY
```

---

### Run the Application

```bash
streamlit run app.py
```

---

# 📊 System Capabilities

✅ Resume Parsing

✅ AI Resume Analysis

✅ Job Description Understanding

✅ Skill Matching

✅ Missing Skill Detection

✅ AI Resume Suggestions

✅ Resume Evaluation

✅ Interactive Dashboard

✅ Live Hosted Deployment

---

# 🎯 Use Cases

- Students
- Fresh Graduates
- Software Engineers
- Data Scientists
- AI Engineers
- Recruiters
- HR Teams
- Career Coaches

---

# 🚀 Future Roadmap

- Resume Ranking
- Recruiter Dashboard
- AI Resume Rewriter
- Cover Letter Generator
- Interview Question Generator
- Resume PDF Report
- Resume History
- Multi Resume Screening
- Multi Language Support
- Job Recommendation Engine

---

# 📸 Screenshots

> Add screenshots of your application here.

Example:

```
assets/dashboard.png

assets/result.png

assets/analysis.png
```

---

# 🤝 Contributing

Contributions are always welcome.

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👩‍💻 Author

## Kajal Maurya

**M.Sc. Data Science**

Artificial Intelligence • Machine Learning • NLP • LLM

📧 **Email:** mauryakajal444@gmail.com

🌐 **GitHub:** https://github.com/Kajal805-M

🚀 **Live Project:** https://shortlistai-ai-based-resume-shortlisting.onrender.com

---

<div align="center">

## ⭐ If this project helped you, please consider giving it a Star!

### 🚀 [**Try ShortlistAI Live**](https://shortlistai-ai-based-resume-shortlisting.onrender.com)

**Built with ❤️ using Python, Streamlit, and Large Language Models**

</div>
