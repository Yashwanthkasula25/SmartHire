🚀 SmartHire – Intelligent Hiring Platform
📌 Overview

SmartHire is a full-stack hiring platform designed to streamline the recruitment process by combining user management, job handling, and AI-driven candidate evaluation.

The system enables recruiters to manage applicants while also leveraging intelligent modules like resume parsing and interview evaluation.

🎯 Features
👤 User & Admin Management
Secure user registration and login
Role-based access (Admin / Recruiter / User)
Profile management
💼 Job & Recruitment
Job posting and listing
Candidate application tracking
Recruiter dashboard
🤖 AI-Based Modules
Resume parsing (resume_parser.py)
Resume scoring system (resume_scoring.py)
AI interview evaluation (ai_interview_evaluator.py)
AI resume scoring (ai_resume_scoring.py)
Candidate ranking / blending (blend_ai.py)
📊 Dashboards
Admin dashboard
Recruiter dashboard
Candidate dashboard
🔐 Security
Authentication system (auth.py)
Security utilities (security.py)
🛠️ Tech Stack
Frontend
HTML
CSS
JavaScript
Backend
Python (FastAPI / Flask-style structure)
Database
SQLAlchemy ORM
Alembic for migrations
📂 Project Structure
SmartHire/
│
├── Backend/
│   ├── app/
│   │   ├── core/              # AI + business logic
│   │   │   ├── resume_parser.py
│   │   │   ├── ai_interview_evaluator.py
│   │   │   ├── ai_resume_scoring.py
│   │   │   ├── resume_scoring.py
│   │   │   ├── blend_ai.py
│   │   │   ├── auth.py
│   │   │   ├── security.py
│   │   │   └── scheduler.py
│   │   │
│   │   ├── db/                # Database configuration
│   │   ├── models/            # Data models
│   │   ├── main.py            # Entry point
│   │
│   ├── alembic/               # Database migrations
│   ├── requirements.txt
│
├── Frontend/
│   ├── css/
│   ├── js/
│   ├── *.html                # UI pages
│
└── README.md
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/Yashwanthkasula25/SmartHire.git
cd SmartHire
2️⃣ Setup Backend
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
3️⃣ Run Server
python app/main.py
4️⃣ Open Frontend

Open Frontend/index.html in browser

🧠 Key Modules Explained
Resume Parser → Extracts candidate data from resumes
AI Resume Scoring → Evaluates candidate profiles
Interview Evaluator → Assesses candidate performance
Blend AI → Combines multiple scores for ranking
👨‍💻 Contributors
Yashwanth Kasula
Vijay Vardhan
📌 Note

This project demonstrates a combination of:

Full-stack development
Database management
AI-based evaluation logic
