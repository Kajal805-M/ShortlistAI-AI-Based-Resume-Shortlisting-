import json
import logging
import os

from resume_analyzer import _ranking, analyze_resume


DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"
MAX_TEXT_CHARS = 14000
logger = logging.getLogger("shortlistai.analyzer")


REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "match_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "summary": {"type": "string"},
        "matched_skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "category": {"type": "string"},
                },
                "required": ["name", "category"],
                "additionalProperties": False,
            },
        },
        "missing_skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "category": {"type": "string"},
                },
                "required": ["name", "category"],
                "additionalProperties": False,
            },
        },
        "score_breakdown": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "score": {"type": "number"},
                    "max": {"type": "number"},
                    "description": {"type": "string"},
                },
                "required": ["label", "score", "max", "description"],
                "additionalProperties": False,
            },
        },
        "suggestions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "priority": {"type": "string", "enum": ["High", "Medium", "Low"]},
                    "title": {"type": "string"},
                    "detail": {"type": "string"},
                },
                "required": ["priority", "title", "detail"],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "match_score",
        "summary",
        "matched_skills",
        "missing_skills",
        "score_breakdown",
        "suggestions",
    ],
    "additionalProperties": False,
}


def analyze_resume_with_llm(resume_text, job_description, filename="resume"):
    logger.info("Building rule-based baseline for %r", filename)
    baseline = analyze_resume(resume_text, job_description, filename)
    logger.info(
        "Rule-based baseline ready score=%s matched=%s missing=%s",
        baseline["match_score"],
        len(baseline["matched_skills"]),
        len(baseline["missing_skills"]),
    )

    api_key = os.environ.get("GROQ_API_KEY")
    use_groq = os.environ.get("USE_GROQ_LLM", "true").lower() not in {"0", "false", "no", "off"}
    if not api_key:
        logger.info("Groq LLM skipped: GROQ_API_KEY is not set")
        baseline["analysis_mode"] = "rules_fallback"
        return baseline
    if not use_groq:
        logger.info("Groq LLM skipped: USE_GROQ_LLM disables it")
        baseline["analysis_mode"] = "rules_fallback"
        return baseline

    try:
        logger.info("Requesting Groq LLM report model=%s", os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL))
        llm_report = _request_llm_report(resume_text, job_description, baseline, api_key)
        report = _finalize_report(llm_report, baseline, filename)
        logger.info(
            "Groq LLM report accepted score=%s matched=%s missing=%s",
            report["match_score"],
            len(report["matched_skills"]),
            len(report["missing_skills"]),
        )
        return report
    except Exception:
        logger.exception("Groq LLM failed; using rule-based fallback")
        baseline["analysis_mode"] = "rules_fallback"
        return baseline


def _request_llm_report(resume_text, job_description, baseline, api_key):
    from groq import Groq

    client = Groq(api_key=api_key, timeout=30.0, max_retries=1)
    response = client.chat.completions.create(
        model=os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL),
        temperature=float(os.environ.get("GROQ_TEMPERATURE", "0.2")),
        max_tokens=1800,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful resume screening assistant. Compare only the provided resume "
                    "and job description. Ignore protected characteristics and do not infer age, gender, "
                    "religion, caste, ethnicity, disability, marital status, or nationality. Score job fit, "
                    "evidence strength, relevant skills, experience alignment, education alignment, and "
                    "resume quality. Return concise, recruiter-useful JSON only."
                ),
            },
            {
                "role": "user",
                "content": _build_prompt(resume_text, job_description, baseline),
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "resume_screening_report",
                "strict": True,
                "schema": REPORT_SCHEMA,
            },
        },
    )
    return json.loads(response.choices[0].message.content or "{}")


def _build_prompt(resume_text, job_description, baseline):
    return f"""
Analyze this candidate for the role and produce a better semantic screening report.

Rules:
- Keep match_score calibrated: 90+ only for exceptional direct evidence, 75+ for strong fit, 50-74 for partial fit, below 50 for weak fit.
- score_breakdown must contain exactly these five labels and max values:
  Skills match / 40, Experience / 20, Job relevance / 20, Education / 10, Resume quality / 10.
- matched_skills should include skills clearly supported by both the resume and job description.
- missing_skills should include important job requirements not clearly supported by the resume.
- suggestions must be practical resume improvements, not generic motivation.
- Do not punish missing information unless the job description asks for it.
- Never mention protected characteristics.

Baseline rule-based report for calibration:
{json.dumps(_compact_baseline(baseline), ensure_ascii=False)}

Resume text:
\"\"\"
{_limit_text(resume_text)}
\"\"\"

Job description:
\"\"\"
{_limit_text(job_description)}
\"\"\"
""".strip()


def _compact_baseline(report):
    return {
        "match_score": report["match_score"],
        "matched_skills": report["matched_skills"],
        "missing_skills": report["missing_skills"],
        "score_breakdown": report["score_breakdown"],
        "summary": report["summary"],
    }


def _limit_text(text):
    text = text.strip()
    if len(text) <= MAX_TEXT_CHARS:
        return text
    return text[:MAX_TEXT_CHARS] + "\n...[truncated for model context]..."


def _finalize_report(llm_report, baseline, filename):
    score = _clamp_int(llm_report.get("match_score"), baseline["match_score"])
    breakdown = _normalize_breakdown(llm_report.get("score_breakdown"), baseline["score_breakdown"])
    matched_skills = _normalize_skills(llm_report.get("matched_skills"), baseline["matched_skills"])
    missing_skills = _normalize_skills(llm_report.get("missing_skills"), baseline["missing_skills"])
    stats = {
        **baseline["stats"],
        "matched": len(matched_skills),
        "required": len(matched_skills) + len(missing_skills),
    }

    report = {
        "file_name": filename,
        "match_score": score,
        "ranking": _ranking(score),
        "verdict": _verdict(score),
        "summary": _text_or_default(llm_report.get("summary"), baseline["summary"]),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score_breakdown": breakdown,
        "suggestions": _normalize_suggestions(llm_report.get("suggestions"), baseline["suggestions"]),
        "stats": stats,
        "disclaimer": "LLM-assisted screening estimate, not a hiring decision. Review candidates holistically and avoid using protected characteristics.",
        "analysis_mode": "groq_llm",
    }
    return report


def _normalize_breakdown(items, fallback):
    expected = [
        ("Skills match", 40),
        ("Experience", 20),
        ("Job relevance", 20),
        ("Education", 10),
        ("Resume quality", 10),
    ]
    if not isinstance(items, list) or len(items) != len(expected):
        return fallback

    normalized = []
    for item, (label, maximum) in zip(items, expected):
        if not isinstance(item, dict):
            return fallback
        normalized.append(
            {
                "label": label,
                "score": round(_clamp_float(item.get("score"), 0, maximum), 1),
                "max": maximum,
                "description": _text_or_default(item.get("description"), f"{label} assessment"),
            }
        )
    return normalized


def _normalize_skills(items, fallback):
    if not isinstance(items, list):
        return fallback

    normalized = []
    seen = set()
    for item in items[:12]:
        if not isinstance(item, dict):
            continue
        name = _text_or_default(item.get("name"), "").strip()
        category = _text_or_default(item.get("category"), "Other").strip()
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        normalized.append({"name": name[:40], "category": category[:40] or "Other"})

    return normalized


def _normalize_suggestions(items, fallback):
    if not isinstance(items, list):
        return fallback

    normalized = []
    for item in items[:6]:
        if not isinstance(item, dict):
            continue
        title = _text_or_default(item.get("title"), "").strip()
        detail = _text_or_default(item.get("detail"), "").strip()
        priority = item.get("priority") if item.get("priority") in {"High", "Medium", "Low"} else "Medium"
        if title and detail:
            normalized.append({"priority": priority, "title": title[:90], "detail": detail[:260]})

    return normalized if normalized else fallback


def _clamp_int(value, fallback):
    try:
        return max(0, min(100, int(round(float(value)))))
    except (TypeError, ValueError):
        return fallback


def _clamp_float(value, minimum, maximum):
    try:
        return max(minimum, min(maximum, float(value)))
    except (TypeError, ValueError):
        return minimum


def _text_or_default(value, default):
    return value if isinstance(value, str) and value.strip() else default


def _verdict(score):
    if score >= 80:
        return {"title": "Highly recommended", "tone": "excellent", "message": "The resume demonstrates strong alignment and merits a priority interview review."}
    if score >= 65:
        return {"title": "Recommended", "tone": "good", "message": "The profile is competitive, with a few gaps worth exploring during screening."}
    if score >= 50:
        return {"title": "Consider", "tone": "fair", "message": "There is useful overlap, but the resume needs stronger evidence for key requirements."}
    return {"title": "Not yet aligned", "tone": "low", "message": "Significant job-specific gaps should be addressed before progressing."}
