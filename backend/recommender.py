"""
recommender.py
---------------
Pure-Python recommendation logic for the Skill Gap Analysis system.

No external AI/API calls are made here — the "intelligence" is a
transparent, rule-based scoring algorithm:

1. Normalize the user's current skills (case-insensitive matching).
2. Compare against the weighted skill requirements of the target role.
3. Compute:
   - Matched skills
   - Missing skills (the "gap"), ranked by importance
   - A readiness/match percentage (weighted)
4. For every missing skill, attach course recommendations from the
   local course catalog, sorted so the most critical skills appear first.
"""

from skill_data import ROLES, COURSES


def _normalize(skill_list):
    """Lowercase + strip every skill so comparisons are case-insensitive."""
    return {s.strip().lower() for s in skill_list if s and s.strip()}


def analyze_skill_gap(current_skills, target_role):
    """
    Core analysis function.

    Args:
        current_skills (list[str]): skills the user already has.
        target_role (str): one of the keys in ROLES.

    Returns:
        dict: full analysis result, ready to be returned as JSON.
    """
    if target_role not in ROLES:
        raise ValueError(f"Unknown role: {target_role}")

    required_skills = ROLES[target_role]
    user_skills_normalized = _normalize(current_skills)

    matched = []
    missing = []

    total_weight = 0
    matched_weight = 0

    for req in required_skills:
        skill_name = req["skill"]
        importance = req["importance"]
        total_weight += importance

        if skill_name.strip().lower() in user_skills_normalized:
            matched.append({"skill": skill_name, "importance": importance})
            matched_weight += importance
        else:
            missing.append({"skill": skill_name, "importance": importance})

    # Rank missing skills by importance (critical first), then alphabetically
    missing.sort(key=lambda x: (-x["importance"], x["skill"]))
    matched.sort(key=lambda x: (-x["importance"], x["skill"]))

    match_percentage = round((matched_weight / total_weight) * 100, 1) if total_weight else 0.0

    # Attach course recommendations for each missing skill
    recommendations = []
    for gap in missing:
        skill_name = gap["skill"]
        courses = COURSES.get(skill_name, [])
        recommendations.append({
            "skill": skill_name,
            "importance": gap["importance"],
            "priority": _priority_label(gap["importance"]),
            "courses": courses,
        })

    readiness_level = _readiness_label(match_percentage)

    return {
        "target_role": target_role,
        "match_percentage": match_percentage,
        "readiness_level": readiness_level,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
        "total_required_skills": len(required_skills),
        "total_matched_skills": len(matched),
        "total_missing_skills": len(missing),
    }


def _priority_label(importance):
    if importance >= 3:
        return "High"
    elif importance == 2:
        return "Medium"
    return "Low"


def _readiness_label(match_percentage):
    if match_percentage >= 85:
        return "Job Ready"
    elif match_percentage >= 60:
        return "Almost There"
    elif match_percentage >= 35:
        return "Developing"
    return "Beginner"


def compare_all_roles(current_skills):
    """
    Bonus utility: rank every role by how well the user's current
    skills already match it. Useful for a 'which role fits me best'
    view, computed with the same offline logic.
    """
    results = []
    for role_name in ROLES:
        analysis = analyze_skill_gap(current_skills, role_name)
        results.append({
            "role": role_name,
            "match_percentage": analysis["match_percentage"],
            "readiness_level": analysis["readiness_level"],
        })
    results.sort(key=lambda x: -x["match_percentage"])
    return results
