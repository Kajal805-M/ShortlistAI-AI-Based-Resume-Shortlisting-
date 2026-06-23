import math
import re
from collections import Counter


SKILL_GROUPS = {
    "Programming": ["python", "java", "javascript", "typescript", "c++", "c#", "golang", "go", "ruby", "php", "swift", "kotlin", "rust", "scala", "r"],
    "Frontend": ["react", "angular", "vue", "next.js", "html", "css", "tailwind", "bootstrap", "redux", "figma"],
    "Backend": ["node.js", "express", "django", "flask", "fastapi", "spring boot", ".net", "rest api", "graphql", "microservices"],
    "Data & AI": ["machine learning", "deep learning", "artificial intelligence", "nlp", "computer vision", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "power bi", "tableau", "data analysis", "data science", "generative ai", "llm"],
    "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ci/cd", "linux", "git", "github actions"],
    "Databases": ["sql", "mysql", "postgresql", "mongodb", "redis", "oracle", "snowflake", "firebase", "dynamodb"],
    "Business": ["project management", "product management", "agile", "scrum", "sales", "marketing", "seo", "financial analysis", "business analysis", "stakeholder management"],
    "Professional": ["communication", "leadership", "problem solving", "teamwork", "analytical", "time management", "presentation", "collaboration", "critical thinking"],
}

ALIASES = {
    "nodejs": "node.js", "node js": "node.js", "reactjs": "react", "react.js": "react",
    "nextjs": "next.js", "next js": "next.js", "postgres": "postgresql", "mongo db": "mongodb",
    "amazon web services": "aws", "google cloud": "gcp", "natural language processing": "nlp",
    "continuous integration": "ci/cd", "continuous delivery": "ci/cd", "restful api": "rest api",
    "sklearn": "scikit-learn", "ms excel": "excel",
}

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have", "in", "is", "it", "of", "on", "or", "our", "that", "the", "this", "to", "we", "will", "with", "you", "your", "role", "job", "work", "team", "candidate", "looking", "required", "preferred", "responsibilities", "skills", "experience", "years",
}

ACTION_VERBS = {
    "achieved", "built", "created", "delivered", "designed", "developed", "drove", "improved", "implemented", "increased", "launched", "led", "managed", "optimized", "reduced", "saved", "scaled", "streamlined", "trained",
}


def analyze_resume(resume_text, job_description, filename="resume"):
    resume_clean = _normalize(resume_text)
    job_clean = _normalize(job_description)
    resume_skills = _extract_skills(resume_clean)
    job_skills = _extract_skills(job_clean)
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    skill_score = _ratio(len(matched), len(job_skills), fallback=55) * 40
    semantic_score = _cosine_similarity(resume_clean, job_clean) * 20
    experience = _experience_score(resume_clean, job_clean)
    education = _education_score(resume_clean, job_clean)
    quality, quality_metrics = _quality_score(resume_text)

    breakdown = [
        _score_item("Skills match", skill_score, 40, "Core and supporting skills found"),
        _score_item("Experience", experience, 20, "Relevant experience and seniority signals"),
        _score_item("Job relevance", semantic_score, 20, "Language similarity with the role"),
        _score_item("Education", education, 10, "Education fit for stated requirements"),
        _score_item("Resume quality", quality, 10, "Structure, impact and readability"),
    ]
    total = round(sum(item["score"] for item in breakdown))
    total = max(0, min(100, total))

    return {
        "file_name": filename,
        "match_score": total,
        "ranking": _ranking(total),
        "verdict": _verdict(total),
        "summary": _summary(total, len(matched), len(job_skills), quality_metrics),
        "matched_skills": [_skill_detail(skill) for skill in matched],
        "missing_skills": [_skill_detail(skill) for skill in missing],
        "score_breakdown": breakdown,
        "suggestions": _suggestions(total, missing, quality_metrics, resume_clean, job_clean),
        "stats": {
            "matched": len(matched),
            "required": len(job_skills),
            "resume_words": len(_tokens(resume_clean)),
            "job_words": len(_tokens(job_clean)),
        },
        "disclaimer": "This is an explainable fit estimate, not a hiring decision. Review candidates holistically and avoid using protected characteristics.",
    }


def _normalize(text):
    text = text.lower().replace("–", "-").replace("—", "-")
    for source, target in ALIASES.items():
        text = re.sub(rf"(?<!\w){re.escape(source)}(?!\w)", target, text)
    return re.sub(r"\s+", " ", text).strip()


def _extract_skills(text):
    found = set()
    for skills in SKILL_GROUPS.values():
        for skill in skills:
            if re.search(rf"(?<![\w+#]){re.escape(skill)}(?![\w+#])", text):
                found.add(skill)
    return found


def _skill_detail(skill):
    category = next((group for group, skills in SKILL_GROUPS.items() if skill in skills), "Other")
    return {"name": skill.upper() if skill in {"aws", "gcp", "sql", "nlp", "llm", "css", "html", "php"} else skill.title(), "category": category}


def _tokens(text):
    return [word for word in re.findall(r"[a-z][a-z0-9+#.-]{1,}", text) if word not in STOP_WORDS]


def _cosine_similarity(first, second):
    first_counts = Counter(_tokens(first))
    second_counts = Counter(_tokens(second))
    shared = set(first_counts) & set(second_counts)
    numerator = sum(first_counts[word] * second_counts[word] for word in shared)
    denominator = math.sqrt(sum(value * value for value in first_counts.values())) * math.sqrt(sum(value * value for value in second_counts.values()))
    if not denominator:
        return 0
    return min(1, numerator / denominator * 2.2)


def _experience_score(resume, job):
    requested = [int(value) for value in re.findall(r"(\d{1,2})\+?\s*(?:years?|yrs?)", job)]
    offered = [int(value) for value in re.findall(r"(\d{1,2})\+?\s*(?:years?|yrs?)", resume)]
    if not requested:
        return 14 if offered else 12
    required = max(requested)
    actual = max(offered, default=0)
    if actual >= required:
        return 20
    if actual:
        return round(8 + (actual / required) * 10, 1)
    return 8


def _education_score(resume, job):
    education_terms = ["bachelor", "master", "phd", "b.tech", "m.tech", "b.e", "mba", "degree", "diploma"]
    job_requires = any(term in job for term in education_terms)
    resume_has = any(term in resume for term in education_terms)
    if not job_requires:
        return 8 if resume_has else 7
    return 10 if resume_has else 3


def _quality_score(original_text):
    lower = original_text.lower()
    word_count = len(_tokens(lower))
    sections = sum(bool(re.search(rf"\b{section}\b", lower)) for section in ["experience", "education", "skills", "projects", "summary"])
    quantified = len(re.findall(r"(?:\b\d+%|\$\s?\d+|\b\d+[kKmM]\+?\b)", original_text))
    action_count = sum(len(re.findall(rf"\b{verb}\b", lower)) for verb in ACTION_VERBS)
    contact = bool(re.search(r"[\w.+-]+@[\w.-]+\.\w+", original_text))
    score = 2 + min(3, sections * 0.6) + min(2, quantified * 0.5) + min(2, action_count * 0.3) + (1 if contact else 0)
    if word_count < 180 or word_count > 1200:
        score -= 1
    return max(0, min(10, round(score, 1))), {"sections": sections, "quantified": quantified, "action_verbs": action_count, "contact": contact, "word_count": word_count}


def _score_item(label, score, maximum, description):
    return {"label": label, "score": round(max(0, min(maximum, score)), 1), "max": maximum, "description": description}


def _ratio(part, whole, fallback=0):
    return fallback / 100 if not whole else part / whole


def _ranking(score):
    if score >= 88:
        return {"label": "Exceptional fit", "percentile": "Top 5%", "tier": "S"}
    if score >= 75:
        return {"label": "Strong contender", "percentile": "Top 15%", "tier": "A"}
    if score >= 62:
        return {"label": "Competitive", "percentile": "Top 35%", "tier": "B"}
    if score >= 45:
        return {"label": "Developing fit", "percentile": "Top 60%", "tier": "C"}
    return {"label": "Low alignment", "percentile": "Needs improvement", "tier": "D"}


def _verdict(score):
    if score >= 80:
        return {"title": "Highly recommended", "tone": "excellent", "message": "The resume demonstrates strong alignment and merits a priority interview review."}
    if score >= 65:
        return {"title": "Recommended", "tone": "good", "message": "The profile is competitive, with a few gaps worth exploring during screening."}
    if score >= 50:
        return {"title": "Consider", "tone": "fair", "message": "There is useful overlap, but the resume needs stronger evidence for key requirements."}
    return {"title": "Not yet aligned", "tone": "low", "message": "Significant job-specific gaps should be addressed before progressing."}


def _summary(score, matched, required, metrics):
    coverage = round(matched / required * 100) if required else 0
    return f"This resume scores {score}/100 with {coverage}% identified skill coverage. It includes {metrics['quantified']} quantified impact signal(s) and {metrics['sections']} standard resume section(s)."


def _suggestions(score, missing, metrics, resume, job):
    suggestions = []
    if missing:
        names = ", ".join(_skill_detail(skill)["name"] for skill in missing[:5])
        suggestions.append({"priority": "High", "title": "Close the most visible skill gaps", "detail": f"If accurate, add evidence of {names} through projects, achievements, or certifications—not a keyword-only list."})
    if metrics["quantified"] < 3:
        suggestions.append({"priority": "High", "title": "Quantify business impact", "detail": "Add measurable outcomes such as revenue, time saved, accuracy, users served, cost reduction, or performance gains."})
    if metrics["action_verbs"] < 4:
        suggestions.append({"priority": "Medium", "title": "Strengthen achievement language", "detail": "Start bullets with decisive verbs such as built, led, improved, optimized, delivered, or launched."})
    if metrics["sections"] < 4:
        suggestions.append({"priority": "Medium", "title": "Improve resume structure", "detail": "Use clear Summary, Skills, Experience, Projects, and Education headings so recruiters and ATS tools can scan quickly."})
    if metrics["word_count"] < 250:
        suggestions.append({"priority": "Medium", "title": "Add relevant evidence", "detail": "The resume is brief. Add concise accomplishments that prove the job-specific responsibilities you can perform."})
    if not metrics["contact"]:
        suggestions.append({"priority": "High", "title": "Add contact information", "detail": "Include a professional email address and relevant profile or portfolio link near the top."})
    if score >= 75 and len(suggestions) < 3:
        suggestions.append({"priority": "Low", "title": "Tailor the opening summary", "detail": "Mirror the role's highest-value outcomes in a concise 2–3 line professional summary."})
    return suggestions[:6]

