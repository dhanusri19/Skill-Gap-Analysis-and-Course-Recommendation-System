import React, { useEffect, useState } from "react";
import "./App.css";
import SkillForm from "./components/SkillForm";
import ResultsDisplay from "./components/ResultsDisplay";
import ResumeUpload from "./components/ResumeUpload";

const API_BASE = "http://localhost:5000/api";

function App() {
  const [roles, setRoles] = useState([]);
  const [result, setResult] = useState(null);
  const [userName, setUserName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("manual"); // "manual" | "resume"
  const [prefillSkills, setPrefillSkills] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/roles`)
      .then((res) => res.json())
      .then((data) => setRoles(data.roles || []))
      .catch(() =>
        setError(
          "Could not reach the backend. Make sure the Flask server is running on port 5000."
        )
      );
  }, []);

  const handleAnalyze = async ({ name, currentSkills, targetRole }) => {
    setLoading(true);
    setError("");
    setUserName(name);

    try {
      const res = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          current_skills: currentSkills,
          target_role: targetRole,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Something went wrong.");
        setResult(null);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError(
        "Could not reach the backend. Make sure the Flask server is running on port 5000."
      );
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Skill Gap Analysis &amp; Course Recommendation System</h1>
        <p>
          Enter your current skills, pick a target job role, and get a
          personalized gap analysis with course recommendations — computed
          entirely with local Python logic, no external AI API required.
        </p>
      </header>

      <div className="tab-switcher">
        <button
          className={activeTab === "manual" ? "tab active" : "tab"}
          onClick={() => setActiveTab("manual")}
        >
          ✍️ Enter Skills Manually
        </button>
        <button
          className={activeTab === "resume" ? "tab active" : "tab"}
          onClick={() => setActiveTab("resume")}
        >
          📄 Upload Resume
        </button>
      </div>

      <main className="app-main">
        <section className="form-section">
          {activeTab === "resume" ? (
            roles.length > 0 && (
              <ResumeUpload
                roles={roles}
                onSkillsExtracted={(skills) => {
                  setPrefillSkills(skills);
                  setActiveTab("manual");
                }}
              />
            )
          ) : roles.length > 0 ? (
            <SkillForm
              roles={roles}
              onAnalyze={handleAnalyze}
              loading={loading}
              prefillSkills={prefillSkills}
            />
          ) : (
            !error && <p>Loading roles...</p>
          )}
          {error && <p className="error-message">{error}</p>}
        </section>

        <section className="result-section">
          <ResultsDisplay result={result} userName={userName} />
        </section>
      </main>

      <footer className="app-footer">
        <p>Built with React (frontend) + Python/Flask (backend)</p>
      </footer>
    </div>
  );
}

export default App;
