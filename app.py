import os

from flask import Flask, jsonify, render_template, request

from file_parser import DocumentParseError, extract_text
from resume_analyzer import analyze_resume


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = {".pdf", ".docx"}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/analyze")
def analyze():
    resume = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()

    if not resume or not resume.filename:
        return jsonify({"error": "Please upload a PDF or DOCX resume."}), 400
    if len(job_description) < 80:
        return jsonify({"error": "Please paste a more complete job description (at least 80 characters)."}), 400

    extension = os.path.splitext(resume.filename.lower())[1]
    if extension not in app.config["UPLOAD_EXTENSIONS"]:
        return jsonify({"error": "Unsupported file type. Please upload a PDF or DOCX file."}), 400

    try:
        resume_text = extract_text(resume.stream, extension)
        if len(resume_text.strip()) < 80:
            return jsonify({"error": "Very little text could be read from this resume. Try a text-based PDF or DOCX file."}), 422
        return jsonify(analyze_resume(resume_text, job_description, resume.filename))
    except DocumentParseError as error:
        return jsonify({"error": str(error)}), 422
    except Exception:
        app.logger.exception("Resume analysis failed")
        return jsonify({"error": "We could not analyze this resume. Please try another file."}), 500


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"error": "The file is too large. Maximum upload size is 8 MB."}), 413


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

