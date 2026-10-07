import React from "react";

/**
 * ResultsDisplay
 * --------------
 * Renders the skill-gap analysis result returned by the Flask backend:
 * match percentage, matched/missing skills, and course recommendations
 * for each missing skill, ranked by priority.
 */
function ResultsDisplay({ result, userName }) {
  if (!result) return null;

  const {
    target_role,
    match_percentage,
    readiness_level,
    matched_skills,
    missing_skills,
    recommendations,
  } = result;

  const greeting = userName ? `${userName}, here` : "Here";

  return (
    <div className="results">
      <h2>
        {greeting} is your gap analysis for{" "}
        <span className="highlight">{target_role}</span>
      </h2>

      <div className="match-summary">
        <div className="match-circle" style={{ "--pct": match_percentage }}>
          <span>{match_percentage}%</span>
        </div>
        <div className="match-text">
          <p className="readiness">
            Readiness Level: <strong>{readiness_level}</strong>
          </p>
          <p>
            {matched_skills.length} of{" "}
            {matched_skills.length + missing_skills.length} required skills
            matched.
          </p>
        </div>
      </div>

      <div className="skill-columns">
        <div className="skill-col matched">
          <h3>✅ Skills You Have ({matched_skills.length})</h3>
          {matched_skills.length === 0 && <p className="empty">None yet.</p>}
          <ul>
            {matched_skills.map((s) => (
              <li key={s.skill}>
                {s.skill}
                <span className={`badge badge-${importanceClass(s.importance)}`}>
                  {importanceLabel(s.importance)}
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="skill-col missing">
          <h3>🎯 Skill Gaps ({missing_skills.length})</h3>
          {missing_skills.length === 0 && (
            <p className="empty">No gaps — you're fully matched!</p>
          )}
          <ul>
            {missing_skills.map((s) => (
              <li key={s.skill}>
                {s.skill}
                <span className={`badge badge-${importanceClass(s.importance)}`}>
                  {importanceLabel(s.importance)}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {recommendations.length > 0 && (
        <div className="recommendations">
          <h3>📚 Recommended Courses (priority order)</h3>
          {recommendations.map((rec) => (
            <div key={rec.skill} className="rec-block">
              <h4>
                {rec.skill}{" "}
                <span className={`badge badge-${importanceClass(rec.importance)}`}>
                  {rec.priority} priority
                </span>
              </h4>
              {rec.courses.length === 0 ? (
                <p className="empty">No course mapped for this skill yet.</p>
              ) : (
                <ul className="course-list">
                  {rec.courses.map((course, idx) => (
                    <li key={idx}>
                      <a href={course.link} target="_blank" rel="noreferrer">
                        {course.title}
                      </a>{" "}
                      — {course.provider} ({course.level}, {course.duration})
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function importanceLabel(importance) {
  if (importance >= 3) return "High";
  if (importance === 2) return "Medium";
  return "Low";
}

function importanceClass(importance) {
  if (importance >= 3) return "high";
  if (importance === 2) return "medium";
  return "low";
}

export default ResultsDisplay;
