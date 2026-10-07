import React, { useState } from "react";

/**
 * SkillForm
 * ---------
 * Collects the user's name (optional), their current skills
 * (comma-separated), and the target role they want to analyze against.
 */
function SkillForm({ roles, onAnalyze, loading, prefillSkills }) {
  const [name, setName] = useState("");
  const [skillsInput, setSkillsInput] = useState("");
  const [targetRole, setTargetRole] = useState(roles[0] || "");

  // If skills were extracted from an uploaded resume, drop them into the field
  React.useEffect(() => {
    if (prefillSkills && prefillSkills.length > 0) {
      setSkillsInput(prefillSkills.join(", "));
    }
  }, [prefillSkills]);

  const handleSubmit = (e) => {
    e.preventDefault();

    const skillsArray = skillsInput
      .split(",")
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    if (skillsArray.length === 0 || !targetRole) {
      alert("Please enter at least one skill and choose a target role.");
      return;
    }

    onAnalyze({ name, currentSkills: skillsArray, targetRole });
  };

  return (
    <form className="skill-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="name">Your Name (optional)</label>
        <input
          id="name"
          type="text"
          placeholder="e.g. Dhanusri"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="skills">Your Current Skills (comma-separated)</label>
        <textarea
          id="skills"
          rows={3}
          placeholder="e.g. Python, SQL, Excel, Statistics"
          value={skillsInput}
          onChange={(e) => setSkillsInput(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="role">Target Role</label>
        <select
          id="role"
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
        >
          {roles.map((role) => (
            <option key={role} value={role}>
              {role}
            </option>
          ))}
        </select>
      </div>

      <button type="submit" className="primary-btn" disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Skill Gap"}
      </button>
    </form>
  );
}

export default SkillForm;
