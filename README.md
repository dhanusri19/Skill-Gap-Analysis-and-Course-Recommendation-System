# Skill Gap Analysis and Course Recommendation System

A full-stack project that compares a user's current skills against the
requirements of a target job role, calculates a skill-gap match score,
and recommends courses to close each gap.

- **Frontend:** React + JSX + CSS
- **Backend:** Python (Flask REST API)
- **Recommendation logic:** Plain rule-based Python (weighted skill
  matching) — **no external AI/LLM API is called anywhere.**
- **NEW: Resume ATS Checker** — upload a `.pdf`/`.docx` resume, auto-extract
  your skills, and get a rule-based ATS compatibility score (0-100) with
  a breakdown and improvement suggestions.
- **NEW: 14 target roles** — Data Analyst, Data Scientist, ML Engineer,
  Business Analyst, Web Developer, AI/NLP Engineer, Data Engineer, BI
  Developer, Product Analyst, Financial Analyst, Cloud Engineer, DevOps
  Engineer, UI/UX Designer, Full Stack Developer.

---

## Project Structure

```
skill-gap-analyzer/
├── backend/
│   ├── app.py            # Flask app + API routes
│   ├── recommender.py    # Core skill-gap analysis logic
│   ├── skill_data.py     # Roles, weighted skills, and course catalog
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── SkillForm.jsx
│   │   │   └── ResultsDisplay.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── README.md
```

---

## How the recommendation logic works

1. Each job role (Data Analyst, Data Scientist, ML Engineer, etc.) has a
   list of required skills, each with an **importance weight** (1–3).
2. The user's entered skills are matched (case-insensitively) against
   the role's requirements.
3. A **match percentage** is computed as:
   `(sum of weights of matched skills / sum of weights of all required skills) * 100`
4. Missing skills are sorted by importance (High → Medium → Low priority).
5. Each missing skill is mapped to 1–2 recommended courses from a local
   course catalog (`skill_data.py`) — title, provider, level, duration, and link.

All of this runs with plain Python `if/else`, dictionaries, and sorting —
no calls to OpenAI, Anthropic, or any other external API.

---

## Prerequisites

- **Python 3.9+** installed and on your PATH
- **Node.js 16+** and **npm** installed
- **VS Code** (recommended, with the Python extension)

---

## Setup & Run — Step by Step (VS Code)

### 1. Open the project folder
Open the `skill-gap-analyzer` folder in VS Code (`File > Open Folder`).

### 2. Run the Backend (Flask API)

Open a terminal in VS Code (`Terminal > New Terminal`) and run:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

- **Windows (PowerShell):**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

Install dependencies and start the server:

```bash
pip install -r requirements.txt
python app.py
```

You should see Flask running at **http://localhost:5000**.
Test it by opening `http://localhost:5000/api/health` in your browser —
you should see `{"status": "ok", ...}`.

### 3. Run the Frontend (React app)

Open a **second** VS Code terminal (keep the backend terminal running)
and run:

```bash
cd frontend
npm install
npm start
```

This will open **http://localhost:3000** in your browser automatically.

### 4. Use the app

1. Enter your name (optional).
2. Enter your current skills, comma-separated (e.g. `Python, SQL, Excel`).
3. Choose a target role (e.g. `Data Analyst`).
4. Click **"Analyze Skill Gap"**.
5. View your match %, matched skills, missing skills, and recommended
   courses for each gap.

---

## API Reference (Backend)

| Method | Endpoint              | Description                                   |
|--------|------------------------|------------------------------------------------|
| GET    | `/api/health`          | Health check                                   |
| GET    | `/api/roles`           | List of all target roles                       |
| GET    | `/api/skills`          | List of all known skills                        |
| POST   | `/api/analyze`         | Body: `{ "current_skills": [...], "target_role": "..." }` |
| POST   | `/api/compare-roles`   | Body: `{ "current_skills": [...] }` — ranks all roles by fit |
| POST   | `/api/upload-resume`   | Multipart form: `resume` file (.pdf/.docx) + optional `target_role` — returns extracted skills, ATS score breakdown, and (if a role was given) a full skill-gap analysis |

### How the ATS score is calculated

The score is out of 100, split across five rule-based factors (same
category of checks real ATS tools use):

| Factor | Max points | What it checks |
|---|---|---|
| Skill Match | 30 | How well detected skills match the target role (or raw skill count if no role given) |
| Resume Sections | 20 | Presence of Education, Experience, Skills, Projects, Certifications |
| Achievements | 20 | Count of strong action verbs and quantified results (numbers/%) |
| Formatting | 20 | Word count in a healthy range + use of bullet points |
| Contact Info | 10 | Presence of email, phone, LinkedIn URL |

The response also includes a `suggestions` list of concrete fixes
(e.g. "Add a clearly labeled 'Projects' section").

---

## Customizing

- **Add/edit roles or required skills:** edit `ROLES` in `backend/skill_data.py`.
- **Add/edit courses:** edit `COURSES` in `backend/skill_data.py`.
- **Change scoring rules:** edit `backend/recommender.py`
  (`analyze_skill_gap`, `_priority_label`, `_readiness_label`).

---

## Troubleshooting

- **"Could not reach the backend"** in the browser → make sure
  `python app.py` is still running in its terminal on port 5000.
- **CORS errors** → `flask-cors` is already enabled in `app.py`; make
  sure you installed `requirements.txt` inside the activated venv.
- **`npm start` fails** → delete `frontend/node_modules` and
  `package-lock.json`, then re-run `npm install`.
