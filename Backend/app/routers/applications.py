from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
import shutil
import os

from ..db.database import get_db
from ..models.application import CandidateApplication
from ..models.interview import Interview
from ..models.job import JobListing
from ..schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    UpdateApplicationStatus
)
from ..core.auth import get_current_user

from ..core.resume_parser import extract_text_from_pdf
from ..core.resume_scoring import calculate_resume_score
from ..core.ai_resume_scoring import analyze_resume_with_ai
from ..core.bland_ai import start_bland_interview
from ..core.voice_scoring import calculate_voice_score
from ..core.interview_analysis import analyze_interview


router = APIRouter(prefix="/applications", tags=["Applications"])


# ============================================================
# Candidate Applies to Job
# ============================================================
@router.post("/", response_model=ApplicationResponse)
def apply_job(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "candidate":
        raise HTTPException(403, "Only candidates can apply")

    job = db.query(JobListing).filter(
        JobListing.id == data.job_id
    ).first()

    if not job:
        raise HTTPException(404, "Job not found")

    application = CandidateApplication(
        user_id=current_user.id,
        job_id=data.job_id,
        resume_url=data.resume_url
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


# ============================================================
# Candidate sees own applications
# ============================================================
@router.get("/my", response_model=list[ApplicationResponse])
def my_applications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(CandidateApplication).filter(
        CandidateApplication.user_id == current_user.id
    ).all()


# ============================================================
# Recruiter sees applicants for a job
# ============================================================
@router.get("/job/{job_id}")
def job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "recruiter":
        raise HTTPException(403, "Not allowed")

    job = db.query(JobListing).filter(
        JobListing.id == job_id,
        JobListing.recruiter_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(404, "Job not found")

    applications = (
        db.query(CandidateApplication)
        .filter(CandidateApplication.job_id == job_id)
        .order_by(
            CandidateApplication.status.desc(),
            CandidateApplication.voice_score.desc().nullslast(),
            CandidateApplication.resume_score.desc()
        )
        .all()
    )

    result = []

    for app in applications:
        result.append({
            "application_id": app.id,
            "candidate_name": app.user.name,

            "resume_score": app.resume_score,
            "interview_score": app.voice_score,

            "communication_score": app.communication_score,
            "technical_score": app.technical_score,
            "confidence_score": app.confidence_score,

            "strengths_and_weakness": app.interview_feedback,

            "status": app.status,
            "applied_at": app.created_at
        })

    return result


# ============================================================
# Upload Resume + Resume AI Scoring
# ============================================================
@router.post("/{application_id}/upload-resume")
def upload_resume(
    application_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    application = db.query(CandidateApplication).filter(
        CandidateApplication.id == application_id,
        CandidateApplication.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(404, "Application not found")

    # ---------- SAVE FILE ----------
    upload_dir = "uploads/resumes"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{application_id}.pdf"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------- EXTRACT TEXT ----------
    resume_text = extract_text_from_pdf(file_path)

    job = application.job

    # ---------- RESUME SCORING ----------
    tfidf_score = calculate_resume_score(
        resume_text,
        job.description or ""
    )

    ai_result = analyze_resume_with_ai(
        resume_text=resume_text,
        job_description=job.description or ""
    )

    ai_score = ai_result["score"]

    resume_final_score = int((0.4 * tfidf_score) + (0.6 * ai_score))

    # ---------- SAVE RESUME DATA ----------
    application.resume_url = file_path
    application.resume_score = resume_final_score
    application.voice_score = None
    application.final_score = None

    candidate = application.user

    print("RESUME SCORE:", resume_final_score)

    # ============================================================
    # ✅ RESUME SHORTLISTING LOGIC
    # ============================================================
    if job.resume_min_score and resume_final_score < job.resume_min_score:

        print("Resume rejected — below minimum score")
        application.status = "rejected"

    else:
        print("Resume shortlisted — starting interview")

        application.status = "interview_in_progress"
        candidate = application.user 
        job = application.job 
    #   START BLAND INTERVIEW
        print("REACHED BLAND SECTION") 
        print("PHONE:", candidate.phone)
        try:
            start_bland_interview(
                phone_number=candidate.phone,
                candidate_name=candidate.name,
                job_title=job.title,
                application_id=application.id
            )
        except Exception as e:
            print("Bland AI failed:", e)

    db.commit()

    return {
        "message": "Resume uploaded and analyzed",
        "resume_score": resume_final_score,
        "status": application.status
    }



# ============================================================
# Recruiter updates application status manually
# ============================================================
@router.patch("/{application_id}/status")
def update_application_status(
    application_id: int,
    data: UpdateApplicationStatus,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "recruiter":
        raise HTTPException(403, "Not allowed")

    application = db.query(CandidateApplication).filter(
        CandidateApplication.id == application_id
    ).first()

    if not application:
        raise HTTPException(404, "Application not found")

    if application.job.recruiter_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    allowed_status = [
    "shortlisted",
    "rejected",
    "hired"
    ]


    if data.status not in allowed_status:
        raise HTTPException(400, "Invalid status")

    application.status = data.status
    db.commit()

    return {"message": "Status updated"}


# ============================================================
# Manual fallback voice score update
# ============================================================
@router.post("/{application_id}/voice-score")
def update_voice_score(
    application_id: int,
    voice_score: int,
    db: Session = Depends(get_db)
):

    application = db.query(CandidateApplication).filter(
        CandidateApplication.id == application_id
    ).first()

    if not application:
        raise HTTPException(404, "Application not found")

    if application.resume_score is None:
        raise HTTPException(400, "Resume score missing")

    job = application.job

    # ---------- SAVE VOICE SCORE ----------
    application.voice_score = voice_score

    # ---------- INTERVIEW DECISION ----------
    if (
        job.interview_min_score and
        voice_score >= job.interview_min_score
    ):
        application.status = "shortlisted"
    else:
        application.status = "rejected"

    db.commit()

    return {
        "voice_score": voice_score,
        "status": application.status
    }


# ============================================================
# Bland AI Webhook (AUTOMATIC FLOW)
# ============================================================

BLAND_WEBHOOK_SECRET = os.getenv("BLAND_WEBHOOK_SECRET")


@router.post("/bland-webhook")
async def bland_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        data = await request.json()
        print("BLAND WEBHOOK DATA:", data)

    except Exception:
        body = await request.body()
        print("Webhook received non-JSON body:", body)
        return {"message": "Ignored non-JSON webhook"}

    # ✅ Process only completed interviews
    status = data.get("status")
    if status != "completed":
        return {"message": "Ignoring non-completed event"}

    # ✅ Extract transcript
    transcript = data.get("concatenated_transcript")

    metadata = data.get("metadata", {})
    application_id = metadata.get("application_id")

    if not application_id or not transcript:
        print("Invalid webhook payload")
        return {"message": "Missing required fields"}

    # ---------- FETCH APPLICATION ----------
    application = db.query(CandidateApplication).filter(
        CandidateApplication.id == application_id
    ).first()

    if not application:
        print("Application not found")
        return {"message": "Application not found"}

    # ---------- SAVE INTERVIEW DATA ----------
    interview = db.query(Interview).filter(
        Interview.candidate_application_id == application.id
    ).first()

    if not interview:
        interview = Interview(
            candidate_application_id=application.id
        )
        db.add(interview)

    interview.transcript = transcript
    interview.duration = int(data.get("corrected_duration", 0))

    interview.started_at = data.get("started_at")
    interview.ended_at = data.get("end_at")


    # ---------- CALCULATE VOICE SCORE ----------
    result = calculate_voice_score(transcript)

    application.voice_score = result["voice_score"]
    application.communication_score = result["communication_score"]
    application.technical_score = result["technical_score"]
    application.confidence_score = result["confidence_score"]
    application.interview_feedback = result["feedback"]

    job = application.job

    # ---------- INTERVIEW ANALYSIS ----------
    analysis = analyze_interview(
        transcript,
        application.voice_score
    )

    interview.strengths = analysis["strengths"]
    interview.weaknesses = analysis["weaknesses"]
    interview.recommendation = analysis["recommendation"]

    # ============================================================
    # ✅ INTERVIEW SHORTLISTING LOGIC (NEW)
    # ============================================================
    if (
        job.interview_min_score and
        application.voice_score >= job.interview_min_score
    ):
        application.status = "shortlisted"
    else:
        application.status = "rejected"

    db.commit()

    return {"message": "Interview processed successfully"}
