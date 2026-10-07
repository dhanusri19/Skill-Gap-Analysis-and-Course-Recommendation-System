"""
skill_data.py
--------------
Static knowledge base used by the recommendation engine.

ROLES:
    Maps a job role -> list of required skills, each with an
    "importance" weight (1 = nice to have, 2 = important, 3 = critical).

COURSES:
    Maps a skill name -> list of recommended courses for that skill.
    Each course has: title, provider, level, duration, link.

This data is intentionally hard-coded (no external API calls) so the
whole system runs fully offline using plain Python logic.
"""

ROLES = {
    "Data Analyst": [
        {"skill": "SQL", "importance": 3},
        {"skill": "Excel", "importance": 3},
        {"skill": "Python", "importance": 2},
        {"skill": "Statistics", "importance": 3},
        {"skill": "Data Visualization", "importance": 3},
        {"skill": "Power BI", "importance": 2},
        {"skill": "Pandas", "importance": 2},
        {"skill": "Communication", "importance": 2},
        {"skill": "Business Acumen", "importance": 1},
    ],
    "Data Scientist": [
        {"skill": "Python", "importance": 3},
        {"skill": "Statistics", "importance": 3},
        {"skill": "Machine Learning", "importance": 3},
        {"skill": "SQL", "importance": 2},
        {"skill": "Data Visualization", "importance": 2},
        {"skill": "Pandas", "importance": 2},
        {"skill": "Deep Learning", "importance": 2},
        {"skill": "Probability", "importance": 3},
        {"skill": "Communication", "importance": 1},
    ],
    "Machine Learning Engineer": [
        {"skill": "Python", "importance": 3},
        {"skill": "Machine Learning", "importance": 3},
        {"skill": "Deep Learning", "importance": 3},
        {"skill": "Deployment", "importance": 2},
        {"skill": "SQL", "importance": 1},
        {"skill": "Statistics", "importance": 2},
        {"skill": "Cloud Computing", "importance": 2},
        {"skill": "Data Structures", "importance": 2},
    ],
    "Business Analyst": [
        {"skill": "Excel", "importance": 3},
        {"skill": "SQL", "importance": 2},
        {"skill": "Business Acumen", "importance": 3},
        {"skill": "Communication", "importance": 3},
        {"skill": "Data Visualization", "importance": 2},
        {"skill": "Power BI", "importance": 2},
        {"skill": "Statistics", "importance": 1},
    ],
    "Web Developer": [
        {"skill": "HTML/CSS", "importance": 3},
        {"skill": "JavaScript", "importance": 3},
        {"skill": "React", "importance": 3},
        {"skill": "Node.js", "importance": 2},
        {"skill": "SQL", "importance": 1},
        {"skill": "Git", "importance": 2},
        {"skill": "REST APIs", "importance": 2},
    ],
    "AI/NLP Engineer": [
        {"skill": "Python", "importance": 3},
        {"skill": "Machine Learning", "importance": 2},
        {"skill": "Deep Learning", "importance": 3},
        {"skill": "NLP", "importance": 3},
        {"skill": "Statistics", "importance": 2},
        {"skill": "Data Structures", "importance": 1},
    ],
    "Data Engineer": [
        {"skill": "Python", "importance": 3},
        {"skill": "SQL", "importance": 3},
        {"skill": "ETL", "importance": 3},
        {"skill": "Cloud Computing", "importance": 3},
        {"skill": "Data Warehousing", "importance": 2},
        {"skill": "Big Data Tools", "importance": 2},
        {"skill": "Data Structures", "importance": 1},
    ],
    "BI Developer": [
        {"skill": "SQL", "importance": 3},
        {"skill": "Power BI", "importance": 3},
        {"skill": "Data Visualization", "importance": 3},
        {"skill": "ETL", "importance": 2},
        {"skill": "Excel", "importance": 2},
        {"skill": "Business Acumen", "importance": 2},
        {"skill": "Communication", "importance": 1},
    ],
    "Product Analyst": [
        {"skill": "SQL", "importance": 3},
        {"skill": "Data Visualization", "importance": 2},
        {"skill": "Statistics", "importance": 2},
        {"skill": "Business Acumen", "importance": 3},
        {"skill": "Communication", "importance": 3},
        {"skill": "Excel", "importance": 1},
        {"skill": "A/B Testing", "importance": 2},
    ],
    "Financial Analyst": [
        {"skill": "Excel", "importance": 3},
        {"skill": "Financial Modeling", "importance": 3},
        {"skill": "SQL", "importance": 2},
        {"skill": "Statistics", "importance": 2},
        {"skill": "Business Acumen", "importance": 3},
        {"skill": "Communication", "importance": 2},
        {"skill": "Data Visualization", "importance": 1},
    ],
    "Cloud Engineer": [
        {"skill": "Cloud Computing", "importance": 3},
        {"skill": "Python", "importance": 2},
        {"skill": "Linux", "importance": 2},
        {"skill": "Networking", "importance": 2},
        {"skill": "Deployment", "importance": 2},
        {"skill": "Data Structures", "importance": 1},
    ],
    "DevOps Engineer": [
        {"skill": "Cloud Computing", "importance": 3},
        {"skill": "Deployment", "importance": 3},
        {"skill": "Git", "importance": 2},
        {"skill": "Linux", "importance": 2},
        {"skill": "Python", "importance": 1},
        {"skill": "Networking", "importance": 1},
    ],
    "UI/UX Designer": [
        {"skill": "Figma", "importance": 3},
        {"skill": "HTML/CSS", "importance": 2},
        {"skill": "Communication", "importance": 2},
        {"skill": "User Research", "importance": 3},
        {"skill": "Wireframing", "importance": 2},
    ],
    "Full Stack Developer": [
        {"skill": "HTML/CSS", "importance": 3},
        {"skill": "JavaScript", "importance": 3},
        {"skill": "React", "importance": 3},
        {"skill": "Node.js", "importance": 3},
        {"skill": "SQL", "importance": 2},
        {"skill": "Git", "importance": 2},
        {"skill": "REST APIs", "importance": 2},
        {"skill": "Deployment", "importance": 1},
    ],
}

COURSES = {
    "SQL": [
        {"title": "SQL for Data Analysis", "provider": "Udacity", "level": "Beginner", "duration": "4 weeks", "link": "https://www.udacity.com/course/sql-for-data-analysis--ud198"},
        {"title": "The Complete SQL Bootcamp", "provider": "Udemy", "level": "Beginner-Intermediate", "duration": "9 hours", "link": "https://www.udemy.com/course/the-complete-sql-bootcamp/"},
    ],
    "Excel": [
        {"title": "Excel Skills for Business", "provider": "Coursera (Macquarie Univ.)", "level": "Beginner", "duration": "5 courses", "link": "https://www.coursera.org/specializations/excel"},
        {"title": "Microsoft Excel - Advanced Excel Formulas", "provider": "Udemy", "level": "Intermediate", "duration": "7 hours", "link": "https://www.udemy.com/course/advanced-excel-formulas-functions/"},
    ],
    "Python": [
        {"title": "Python for Everybody", "provider": "Coursera (Univ. of Michigan)", "level": "Beginner", "duration": "8 months (self-paced)", "link": "https://www.coursera.org/specializations/python"},
        {"title": "100 Days of Code: Python", "provider": "Udemy", "level": "Beginner-Advanced", "duration": "60 hours", "link": "https://www.udemy.com/course/100-days-of-code/"},
    ],
    "Statistics": [
        {"title": "Statistics with Python Specialization", "provider": "Coursera (Univ. of Michigan)", "level": "Intermediate", "duration": "3 courses", "link": "https://www.coursera.org/specializations/statistics-with-python"},
        {"title": "Introduction to Statistics", "provider": "Khan Academy", "level": "Beginner", "duration": "Self-paced", "link": "https://www.khanacademy.org/math/statistics-probability"},
    ],
    "Data Visualization": [
        {"title": "Data Visualization with Python", "provider": "IBM (Coursera)", "level": "Intermediate", "duration": "4 weeks", "link": "https://www.coursera.org/learn/python-for-data-visualization"},
        {"title": "Storytelling with Data", "provider": "Udemy", "level": "Beginner", "duration": "5 hours", "link": "https://www.udemy.com/course/data-storytelling/"},
    ],
    "Power BI": [
        {"title": "Microsoft Power BI Desktop for Business Intelligence", "provider": "Udemy", "level": "Beginner", "duration": "18 hours", "link": "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/"},
        {"title": "Power BI Professional Certificate", "provider": "Microsoft (Coursera)", "level": "Beginner-Intermediate", "duration": "8 courses", "link": "https://www.coursera.org/professional-certificates/microsoft-power-bi-data-analyst"},
    ],
    "Pandas": [
        {"title": "Data Analysis with Python (Pandas)", "provider": "freeCodeCamp", "level": "Beginner-Intermediate", "duration": "10 hours", "link": "https://www.freecodecamp.org/learn/data-analysis-with-python/"},
        {"title": "Pandas Data Wrangling", "provider": "DataCamp", "level": "Intermediate", "duration": "4 hours", "link": "https://www.datacamp.com/courses/data-manipulation-with-pandas"},
    ],
    "Communication": [
        {"title": "Business Communication Skills", "provider": "Coursera", "level": "Beginner", "duration": "4 courses", "link": "https://www.coursera.org/specializations/business-communication"},
        {"title": "Improve Your Presentation Skills", "provider": "Udemy", "level": "Beginner", "duration": "3 hours", "link": "https://www.udemy.com/course/presentation-skills-course/"},
    ],
    "Business Acumen": [
        {"title": "Business Analytics Specialization", "provider": "Coursera (Wharton)", "level": "Intermediate", "duration": "5 courses", "link": "https://www.coursera.org/specializations/business-analytics"},
    ],
    "Machine Learning": [
        {"title": "Machine Learning Specialization", "provider": "Coursera (Andrew Ng / DeepLearning.AI)", "level": "Intermediate", "duration": "3 courses", "link": "https://www.coursera.org/specializations/machine-learning-introduction"},
        {"title": "Hands-On Machine Learning", "provider": "Udemy", "level": "Intermediate", "duration": "20 hours", "link": "https://www.udemy.com/course/machinelearning/"},
    ],
    "Deep Learning": [
        {"title": "Deep Learning Specialization", "provider": "Coursera (DeepLearning.AI)", "level": "Advanced", "duration": "5 courses", "link": "https://www.coursera.org/specializations/deep-learning"},
        {"title": "PyTorch for Deep Learning", "provider": "Udemy", "level": "Intermediate-Advanced", "duration": "24 hours", "link": "https://www.udemy.com/course/pytorch-for-deep-learning/"},
    ],
    "Probability": [
        {"title": "Probability - The Science of Uncertainty", "provider": "edX (MIT)", "level": "Intermediate", "duration": "16 weeks", "link": "https://www.edx.org/learn/probability/massachusetts-institute-of-technology-probability-the-science-of-uncertainty-and-data"},
    ],
    "Deployment": [
        {"title": "MLOps Specialization", "provider": "Coursera (DeepLearning.AI)", "level": "Advanced", "duration": "4 courses", "link": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops"},
    ],
    "Cloud Computing": [
        {"title": "AWS Certified Cloud Practitioner", "provider": "AWS Training", "level": "Beginner", "duration": "Self-paced", "link": "https://aws.amazon.com/certification/certified-cloud-practitioner/"},
        {"title": "Google Cloud Fundamentals", "provider": "Coursera (Google Cloud)", "level": "Beginner", "duration": "4 weeks", "link": "https://www.coursera.org/learn/gcp-fundamentals"},
    ],
    "Data Structures": [
        {"title": "Data Structures and Algorithms", "provider": "Coursera (UC San Diego)", "level": "Intermediate", "duration": "6 courses", "link": "https://www.coursera.org/specializations/data-structures-algorithms"},
    ],
    "HTML/CSS": [
        {"title": "Responsive Web Design", "provider": "freeCodeCamp", "level": "Beginner", "duration": "300 hours", "link": "https://www.freecodecamp.org/learn/2022/responsive-web-design/"},
    ],
    "JavaScript": [
        {"title": "The Complete JavaScript Course", "provider": "Udemy", "level": "Beginner-Advanced", "duration": "69 hours", "link": "https://www.udemy.com/course/the-complete-javascript-course/"},
    ],
    "React": [
        {"title": "React - The Complete Guide", "provider": "Udemy", "level": "Beginner-Advanced", "duration": "48 hours", "link": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"},
    ],
    "Node.js": [
        {"title": "Node.js, Express, MongoDB & More", "provider": "Udemy", "level": "Intermediate", "duration": "42 hours", "link": "https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/"},
    ],
    "Git": [
        {"title": "Git & GitHub Crash Course", "provider": "Udemy", "level": "Beginner", "duration": "4 hours", "link": "https://www.udemy.com/course/git-and-github-bootcamp/"},
    ],
    "REST APIs": [
        {"title": "REST APIs with Flask and Python", "provider": "Udemy", "level": "Intermediate", "duration": "15 hours", "link": "https://www.udemy.com/course/rest-api-flask-and-python/"},
    ],
    "NLP": [
        {"title": "Natural Language Processing Specialization", "provider": "Coursera (DeepLearning.AI)", "level": "Advanced", "duration": "4 courses", "link": "https://www.coursera.org/specializations/natural-language-processing"},
    ],
    "ETL": [
        {"title": "ETL and Data Pipelines with Shell, Airflow and Kafka", "provider": "IBM (Coursera)", "level": "Intermediate", "duration": "4 weeks", "link": "https://www.coursera.org/learn/etl-and-data-pipelines-shell-airflow-kafka"},
    ],
    "Data Warehousing": [
        {"title": "Data Warehouse Concepts, Design, and Data Integration", "provider": "Coursera (Univ. of Colorado)", "level": "Intermediate", "duration": "4 weeks", "link": "https://www.coursera.org/learn/dwdesign"},
    ],
    "Big Data Tools": [
        {"title": "Big Data Specialization (Hadoop & Spark)", "provider": "Coursera (UC San Diego)", "level": "Intermediate", "duration": "6 courses", "link": "https://www.coursera.org/specializations/big-data"},
    ],
    "A/B Testing": [
        {"title": "A/B Testing", "provider": "Udacity", "level": "Intermediate", "duration": "4 weeks", "link": "https://www.udacity.com/course/ab-testing--ud257"},
    ],
    "Financial Modeling": [
        {"title": "Financial Modeling & Valuation", "provider": "Coursera (Wharton)", "level": "Intermediate", "duration": "4 courses", "link": "https://www.coursera.org/specializations/business-valuation-corporate-finance"},
    ],
    "Linux": [
        {"title": "Linux Command Line Basics", "provider": "Udacity", "level": "Beginner", "duration": "2 weeks", "link": "https://www.udacity.com/course/linux-command-line-basics--ud595"},
    ],
    "Networking": [
        {"title": "Computer Networking Fundamentals", "provider": "Coursera (Google)", "level": "Beginner", "duration": "4 weeks", "link": "https://www.coursera.org/learn/networking-fundamentals"},
    ],
    "Figma": [
        {"title": "UI/UX Design Specialization (Figma)", "provider": "Coursera (CalArts)", "level": "Beginner", "duration": "6 courses", "link": "https://www.coursera.org/specializations/ui-ux-design"},
    ],
    "User Research": [
        {"title": "UX Research at Scale", "provider": "Coursera (Google)", "level": "Intermediate", "duration": "4 weeks", "link": "https://www.coursera.org/learn/ux-research-at-scale"},
    ],
    "Wireframing": [
        {"title": "Wireframing and Prototyping", "provider": "Coursera (Google)", "level": "Beginner", "duration": "3 weeks", "link": "https://www.coursera.org/learn/wireframing-and-prototyping"},
    ],
}


def get_all_skills():
    """Return a sorted list of every unique skill across all roles."""
    skills = set()
    for role_skills in ROLES.values():
        for entry in role_skills:
            skills.add(entry["skill"])
    return sorted(skills)


def get_all_roles():
    """Return a sorted list of all available role names."""
    return sorted(ROLES.keys())
