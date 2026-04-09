🚀 SmartHire – Intelligent Hiring Platform
📌 Overview

SmartHire is a full-stack hiring platform designed to streamline the recruitment process by combining user management, job handling, and AI-driven candidate evaluation.

The system enables recruiters to manage applicants while leveraging intelligent modules like resume parsing and interview evaluation.

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
Resume parsing
Resume scoring
AI interview evaluation
Candidate ranking / blending
📊 Dashboards
Admin dashboard
Recruiter dashboard
Candidate dashboard
🔐 Security
Authentication system
Security utilities
🛠️ Tech Stack

Frontend

HTML
CSS
JavaScript

Backend

Python

Database

SQLAlchemy (ORM)
Alembic (Migrations)


📂 Project Structure
SmartHire/
│
├── Backend/
│   ├── app/
│   │   ├── core/          # AI & business logic
│   │   ├── db/            # Database config
│   │   ├── models/        # Data models
│   │   └── main.py        # Entry point
│   │
│   ├── alembic/           # DB migrations
│   └── requirements.txt
│
├── Frontend/
│   ├── css/
│   ├── js/
│   └── *.html
│
└── README.md


⚙️ Installation & Setup
1. Clone Repository
git clone https://github.com/Yashwanthkasula25/SmartHire.git
cd SmartHire
2. Setup Backend
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
3. Run Server
python app/main.py
4. Open Frontend

Open Frontend/index.html in your browser

🧠 Key Modules
Resume Parser → Extracts candidate data from resumes
Resume Scoring → Evaluates candidate profiles
Interview Evaluator → Assesses candidate performance
Blend AI → Combines scores for ranking
👨‍💻 Contributors
Yashwanth Kasula
Vijay Vardhan
📌 Note

This project demonstrates:

Full-stack development
Database management
AI-based evaluation logic
