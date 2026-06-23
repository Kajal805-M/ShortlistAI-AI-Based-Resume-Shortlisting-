import io
import unittest

from docx import Document

from app import app
from resume_analyzer import analyze_resume


RESUME = """
Jordan Lee
jordan@example.com
Professional Summary
Python backend engineer with 5 years of experience building cloud services.
Skills
Python, Flask, REST API, PostgreSQL, AWS, Docker, Git, Agile, communication
Experience
Senior Software Engineer — built and launched APIs that reduced latency by 35% and served 50K users.
Led a team of 4 engineers and improved deployment time by 60%.
Projects
Developed a machine learning recommendation service using pandas and scikit-learn.
Education
Bachelor of Technology in Computer Science
"""

JOB = """
We are hiring a Python Backend Engineer with 3+ years of experience. The candidate will
develop REST API services using Python and Flask, work with PostgreSQL, Docker and AWS,
and collaborate in an Agile team. Strong communication, Git, Kubernetes, and problem
solving skills are required. A bachelor's degree is preferred.
"""


class AnalyzerTests(unittest.TestCase):
    def test_analysis_returns_explainable_report(self):
        result = analyze_resume(RESUME, JOB, "jordan.docx")
        self.assertGreaterEqual(result["match_score"], 70)
        self.assertEqual(len(result["score_breakdown"]), 5)
        matched_names = {skill["name"] for skill in result["matched_skills"]}
        missing_names = {skill["name"] for skill in result["missing_skills"]}
        self.assertIn("Python", matched_names)
        self.assertIn("Kubernetes", missing_names)
        self.assertTrue(result["suggestions"])

    def test_api_rejects_missing_file(self):
        client = app.test_client()
        response = client.post("/api/analyze", data={"job_description": JOB})
        self.assertEqual(response.status_code, 400)

    def test_api_analyzes_docx(self):
        document = Document()
        for line in RESUME.splitlines():
            document.add_paragraph(line)
        stream = io.BytesIO()
        document.save(stream)
        stream.seek(0)

        client = app.test_client()
        response = client.post(
            "/api/analyze",
            data={"job_description": JOB, "resume": (stream, "jordan.docx")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("match_score", response.get_json())


if __name__ == "__main__":
    unittest.main()

