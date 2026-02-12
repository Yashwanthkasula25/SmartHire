from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def analyze_resume_with_ai(resume_text: str, job_description: str):
    prompt = f"""
    Compare the resume with the job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Give:
    1. Match score out of 100
    2. Missing skills
    3. Short explanation

    IMPORTANT:
    Return ONLY valid JSON. No extra text.

    Format:
    {{
        "score": number,
        "missing_skills": [],
        "reason": ""
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        result_text = response.text.strip()
        result_json = json.loads(result_text)

        return result_json

    except Exception as e:
        print("AI Resume Scoring Failed:", e)
        return {
            "score": 60,
            "missing_skills": [],
            "reason": "AI scoring temporarily unavailable"
        }
