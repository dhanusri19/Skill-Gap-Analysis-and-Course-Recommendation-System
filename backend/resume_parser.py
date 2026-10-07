"""
resume_parser.py
-----------------
Extracts text from an uploaded resume (PDF or DOCX), detects which known
skills appear in it, and computes a rule-based ATS (Applicant Tracking
System) compatibility score.

Everything here is local, offline logic:
    - pdfplumber / python-docx for text extraction
    - simple keyword/regex matching for skill detection
    - a weighted rubric for the ATS score

No external AI/API calls are made.
"""

import re
import io
import pdfplumber
import docx

from skill_data import get_all_skills

# Sections an ATS-friendly resume is expected to have
EXPECTED_SECTIONS = [
    "education",
    "experience",
    "skills",
    "projects",
    "certifications",
]

# A small set of strong action verbs used to reward achievement-oriented
# bullet points (a real ATS/recruiter heuristic)
ACTION_VERBS = [
    "developed", "built", "designed", "implemented", "led", "managed",
    "created", "analyzed", "improved", "optimized", "automated", "deployed",
    "achieved", "increased", "reduced", "launched", "collaborated",
    "engineered", "architected", "delivered", "researched", "streamlined",
]

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
LINKEDIN_REGEX = r"linkedin\.com/in/[A-Za-z0-9\-_/]+"


def extract_text_from_pdf(file_stream):
    """Extract raw text from an in-memory PDF file stream."""
    text_parts = []
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_stream):
    """Extract raw text from an in-memory DOCX file stream."""
    document = docx.Document(file_stream)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text(filename, file_bytes):
    """Dispatch to the right extractor based on file extension."""
    stream = io.BytesIO(file_bytes)
    lower_name = filename.lower()

    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(stream)
    elif lower_name.endswith(".docx"):
        return extract_text_from_docx(stream)
    else:
        raise ValueError("Unsupported file type. Please upload a .pdf or .docx resume.")


def extract_skills_from_text(text):
    """
    Detect which known skills (from skill_data.get_all_skills()) appear
    in the resume text. Matching is case-insensitive and handles skills
    that contain slashes or multiple words (e.g. 'HTML/CSS').
    """
    text_lower = text.lower()
    found_skills = []

    for skill in get_all_skills():
        skill_lower = skill.lower()
        # Handle compound skills like "HTML/CSS" by checking each part too,
        # but only split-parts longer than 2 chars (avoids false hits like
        # the standalone letters "a"/"b" inside "A/B Testing")
        parts = [skill_lower] + [p for p in skill_lower.split("/") if len(p.strip()) > 2]
        if any(re.search(r"\b" + re.escape(part.strip()) + r"\b", text_lower) for part in parts if part.strip()):
            found_skills.append(skill)

    return sorted(set(found_skills))


def _section_score(text_lower):
    found = [s for s in EXPECTED_SECTIONS if s in text_lower]
    score = round((len(found) / len(EXPECTED_SECTIONS)) * 20, 1)  # out of 20
    return score, found, [s for s in EXPECTED_SECTIONS if s not in found]


def _contact_info_score(text):
    has_email = bool(re.search(EMAIL_REGEX, text))
    has_phone = bool(re.search(PHONE_REGEX, text))
    has_linkedin = bool(re.search(LINKEDIN_REGEX, text, re.IGNORECASE))

    score = 0
    if has_email:
        score += 5
    if has_phone:
        score += 3
    if has_linkedin:
        score += 2
    return score, {"email": has_email, "phone": has_phone, "linkedin": has_linkedin}  # out of 10


def _formatting_score(text):
    """
    Rough, offline proxy for ATS-friendliness of formatting:
    - reasonable word count (not too short, not excessively long)
    - presence of bullet-like structure (lines starting with -, *, •)
    """
    words = text.split()
    word_count = len(words)

    if 250 <= word_count <= 1200:
        length_score = 12
    elif 150 <= word_count < 250 or 1200 < word_count <= 1600:
        length_score = 8
    else:
        length_score = 4

    bullet_lines = len(re.findall(r"(^|\n)\s*[-*•]", text))
    bullet_score = 8 if bullet_lines >= 5 else (5 if bullet_lines >= 2 else 2)

    return length_score + bullet_score, {"word_count": word_count, "bullet_lines": bullet_lines}  # out of 20


def _achievement_score(text_lower):
    verb_hits = sum(1 for v in ACTION_VERBS if v in text_lower)
    number_hits = len(re.findall(r"\b\d+%?\b", text_lower))

    verb_score = min(verb_hits, 10) * 1.0  # up to 10
    number_score = min(number_hits, 10) * 1.0  # up to 10
    return round(verb_score + number_score, 1), {"action_verbs_found": verb_hits, "numbers_found": number_hits}  # out of 20


def _skill_match_score(matched_skills, target_role_analysis):
    """
    Reuses the existing skill-gap match_percentage (0-100) and scales
    it into a 30-point ATS sub-score, since keyword/skill match against
    the target role is the single heaviest-weighted factor in most
    real-world ATS systems.
    """
    if target_role_analysis is None:
        # No target role given — fall back to raw skill count found
        return min(len(matched_skills), 15) * 2.0  # up to 30
    return round((target_role_analysis["match_percentage"] / 100) * 30, 1)


def calculate_ats_score(text, matched_skills, target_role_analysis=None):
    """
    Combine all sub-scores into a final ATS score out of 100, with a
    breakdown so the UI can explain *why* the score is what it is.
    """
    text_lower = text.lower()

    section_pts, sections_found, sections_missing = _section_score(text_lower)
    contact_pts, contact_details = _contact_info_score(text)
    format_pts, format_details = _formatting_score(text)
    achievement_pts, achievement_details = _achievement_score(text_lower)
    skill_pts = _skill_match_score(matched_skills, target_role_analysis)

    total = round(section_pts + contact_pts + format_pts + achievement_pts + skill_pts, 1)
    total = min(total, 100.0)

    return {
        "ats_score": total,
        "rating": _ats_rating(total),
        "breakdown": {
            "skill_match": {"score": skill_pts, "max": 30},
            "sections": {"score": section_pts, "max": 20, "found": sections_found, "missing": sections_missing},
            "achievements": {"score": achievement_pts, "max": 20, "details": achievement_details},
            "formatting": {"score": format_pts, "max": 20, "details": format_details},
            "contact_info": {"score": contact_pts, "max": 10, "details": contact_details},
        },
        "suggestions": _generate_suggestions(sections_missing, contact_details, format_details, achievement_details),
    }


def _ats_rating(score):
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Needs Improvement"
    return "Poor"


def _generate_suggestions(sections_missing, contact_details, format_details, achievement_details):
    suggestions = []

    for section in sections_missing:
        suggestions.append(f"Add a clearly labeled '{section.title()}' section.")

    if not contact_details["email"]:
        suggestions.append("Add a professional email address.")
    if not contact_details["phone"]:
        suggestions.append("Add a phone number.")
    if not contact_details["linkedin"]:
        suggestions.append("Add your LinkedIn profile URL.")

    if format_details["bullet_lines"] < 5:
        suggestions.append("Use more bullet points to describe your experience and projects.")
    if format_details["word_count"] < 250:
        suggestions.append("Your resume looks too short — add more detail on projects/experience.")
    elif format_details["word_count"] > 1200:
        suggestions.append("Your resume looks too long — trim it to the most relevant content.")

    if achievement_details["action_verbs_found"] < 5:
        suggestions.append("Start more bullet points with strong action verbs (e.g. 'Built', 'Led', 'Improved').")
    if achievement_details["numbers_found"] < 3:
        suggestions.append("Quantify your achievements with numbers/percentages where possible.")

    return suggestions
