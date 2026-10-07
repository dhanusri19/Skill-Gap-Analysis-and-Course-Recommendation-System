"""
app.py
------
Flask backend for the Skill Gap Analysis and Course Recommendation System.

Endpoints:
    GET  /api/health          -> simple health check
    GET  /api/roles           -> list of available target roles
    GET  /api/skills          -> list of all known skills (for autocomplete)
    POST /api/analyze         -> run skill-gap analysis for one role
    POST /api/compare-roles   -> rank all roles by current fit

All logic is local/offline (see recommender.py) — no external AI API
is called anywhere in this backend.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from skill_data import get_all_roles, get_all_skills
from recommender import analyze_skill_gap, compare_all_roles
from resume_parser import extract_text, extract_skills_from_text, calculate_ats_score

ALLOWED_RESUME_EXTENSIONS = {".pdf", ".docx"}
MAX_RESUME_SIZE_MB = 5

app = Flask(__name__)
CORS(app)  # allow the React dev server (different port) to call this API


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Skill Gap Analyzer backend is running"})


@app.route("/api/roles", methods=["GET"])
def roles():
    return jsonify({"roles": get_all_roles()})


@app.route("/api/skills", methods=["GET"])
def skills():
    return jsonify({"skills": get_all_skills()})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}

    current_skills = data.get("current_skills", [])
    target_role = data.get("target_role", "")

    if not isinstance(current_skills, list) or not current_skills:
        return jsonify({"error": "Please provide a non-empty list of current_skills."}), 400

    if not target_role:
        return jsonify({"error": "Please provide a target_role."}), 400

    try:
        result = analyze_skill_gap(current_skills, target_role)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(result)


@app.route("/api/compare-roles", methods=["POST"])
def compare_roles():
    data = request.get_json(silent=True) or {}
    current_skills = data.get("current_skills", [])

    if not isinstance(current_skills, list) or not current_skills:
        return jsonify({"error": "Please provide a non-empty list of current_skills."}), 400

    result = compare_all_roles(current_skills)
    return jsonify({"roles_ranked": result})


@app.route("/api/upload-resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded. Attach it as 'resume'."}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    filename_lower = file.filename.lower()
    if not any(filename_lower.endswith(ext) for ext in ALLOWED_RESUME_EXTENSIONS):
        return jsonify({"error": "Only .pdf and .docx files are supported."}), 400

    file_bytes = file.read()
    if len(file_bytes) > MAX_RESUME_SIZE_MB * 1024 * 1024:
        return jsonify({"error": f"File too large. Max {MAX_RESUME_SIZE_MB}MB."}), 400

    # Optional: score against a specific target role, otherwise generic
    target_role = request.form.get("target_role", "").strip()

    try:
        text = extract_text(file.filename, file_bytes)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not text.strip():
        return jsonify({"error": "Could not extract any text from this file. Try a different resume file."}), 400

    matched_skills = extract_skills_from_text(text)

    role_analysis = None
    if target_role:
        try:
            role_analysis = analyze_skill_gap(matched_skills, target_role)
        except ValueError:
            role_analysis = None  # unknown role — skip gap analysis, still score ATS

    ats_result = calculate_ats_score(text, matched_skills, role_analysis)

    return jsonify({
        "extracted_skills": matched_skills,
        "skill_gap_analysis": role_analysis,
        "ats_result": ats_result,
    })


if __name__ == "__main__":
    # Runs on http://localhost:5000
    app.run(debug=True, port=5000)
