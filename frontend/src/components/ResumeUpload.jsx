import React, { useState } from "react";

const API_BASE = "http://localhost:5000/api";

/**
 * ResumeUpload
 * ------------
 * Lets the user upload a .pdf/.docx resume. Sends it to the backend,
 * which extracts text, detects known skills, and computes an ATS
 * compatibility score with a breakdown + suggestions.
 *
 * On success, offers a button to feed the extracted skills straight
 * into the skill-gap analysis (via onSkillsExtracted callback).
 */
function ResumeUpload({ roles, onSkillsExtracted }) {
  const [file, setFile] = useState(null);
  const [targetRole, setTargetRole] = useState(roles[0] || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [data, setData] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0] || null);
    setData(null);
    setError("");
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please choose a .pdf or .docx resume file first.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);
    if (targetRole) formData.append("target_role", targetRole);

    setLoading(true);
    setError("");
    setData(null);

    try {
      const res = await fetch(`${API_BASE}/upload-resume`, {
        method: "POST",
        body: formData,
      });
      const json = await res.json();

      if (!res.ok) {
        setError(json.error || "Something went wrong analyzing the resume.");
      } else {
        setData(json);
      }
    } catch (err) {
      setError(
        "Could not reach the backend. Make sure the Flask server is running on port 5000."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="resume-upload">
      <h2>📄 Resume ATS Checker &amp; Skill Extractor</h2>
      <p className="subtext">
        Upload your resume to get an ATS compatibility score and
        auto-extract your skills for gap analysis.
      </p>

      <form onSubmit={handleUpload} className="resume-form">
        <div className="form-group">
          <label htmlFor="resume-file">Resume File (.pdf or .docx)</label>
          <input
            id="resume-file"
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="resume-role">Score against role (optional)</label>
          <select
            id="resume-role"
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
          >
            <option value="">-- Generic score (no role) --</option>
            {roles.map((role) => (
              <option key={role} value={role}>
                {role}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" className="primary-btn" disabled={loading}>
          {loading ? "Analyzing Resume..." : "Analyze Resume"}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}

      {data && (
        <div className="ats-results">
          <div className="match-summary">
            <div
              className="match-circle"
              style={{ "--pct": data.ats_result.ats_score }}
            >
              <span>{data.ats_result.ats_score}</span>
            </div>
            <div className="match-text">
              <p className="readiness">
                ATS Rating: <strong>{data.ats_result.rating}</strong>
              </p>
              <p>Score is out of 100.</p>
            </div>
          </div>

          <h3>Score Breakdown</h3>
          <ul className="ats-breakdown">
            {Object.entries(data.ats_result.breakdown).map(([key, val]) => (
              <li key={key}>
                <span className="ats-label">{formatLabel(key)}</span>
                <span className="ats-bar-wrap">
                  <span
                    className="ats-bar"
                    style={{ width: `${(val.score / val.max) * 100}%` }}
                  />
                </span>
                <span className="ats-score-text">
                  {val.score} / {val.max}
                </span>
              </li>
            ))}
          </ul>

          {data.ats_result.suggestions.length > 0 && (
            <div className="suggestions">
              <h3>💡 Suggestions to Improve</h3>
              <ul>
                {data.ats_result.suggestions.map((s, idx) => (
                  <li key={idx}>{s}</li>
                ))}
              </ul>
            </div>
          )}

          <h3>Skills Detected in Resume ({data.extracted_skills.length})</h3>
          {data.extracted_skills.length === 0 ? (
            <p className="empty">No known skills detected.</p>
          ) : (
            <div className="skill-chips">
              {data.extracted_skills.map((s) => (
                <span key={s} className="chip">
                  {s}
                </span>
              ))}
            </div>
          )}

          {data.extracted_skills.length > 0 && (
            <button
              type="button"
              className="secondary-btn"
              onClick={() => onSkillsExtracted(data.extracted_skills)}
            >
              Use These Skills for Gap Analysis →
            </button>
          )}
        </div>
      )}
    </div>
  );
}

function formatLabel(key) {
  const labels = {
    skill_match: "Skill Match",
    sections: "Resume Sections",
    achievements: "Achievements & Action Verbs",
    formatting: "Formatting",
    contact_info: "Contact Info",
  };
  return labels[key] || key;
}

export default ResumeUpload;
