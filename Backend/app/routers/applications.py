from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os


from ..db.database import get_db
from ..models.application import CandidateApplication
from ..models.job import JobListing
from ..models.user import User
from ..schemas.application import ApplicationCreate, ApplicationResponse
from ..core.auth import get_current_user

from ..core.resume_parser import extract_text_from_pdf
from ..core.resume_scoring import calculate_resume_score
from ..core.ai_resume_scoring import analyze_resume_with_ai


router = APIRouter(prefix="/applications", tags=["Applications"])



# POST /applications → Candidate applies
@router.post("/", response_model=ApplicationResponse)
def apply_job(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = current_user["id"]
    # check user exists
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # allow only candidates
    if user.role != "candidate":
        raise HTTPException(
            status_code=403,
            detail="Only candidates can apply to jobs"
        )

    # check job exists
    job = db.query(JobListing).filter(
        JobListing.id == data.job_id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    application = CandidateApplication(
        user_id=user_id,
        job_id=data.job_id,
        resume_url=data.resume_url
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application

# GET /applications/my → Candidate sees own applications
@router.get("/my", response_model=list[ApplicationResponse])
def my_applications(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(CandidateApplication).filter(
        CandidateApplication.user_id == user_id
    ).all()


# Recruiter — See Applicants for Job
@router.get("/job/{job_id}", response_model=list[ApplicationResponse])
def job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    job = db.query(JobListing).filter(
        JobListing.id == job_id,
        JobListing.recruiter_id == user_id
    ).first()

    if not job:
        raise HTTPException(status_code=403, detail="Not allowed")

    return db.query(CandidateApplication).filter(
        CandidateApplication.job_id == job_id
    ).all()



# upload_resume()
@router.post("/{application_id}/upload-resume")
def upload_resume(
    application_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    application = db.query(CandidateApplication).filter(
    CandidateApplication.id == application_id,
    CandidateApplication.user_id == current_user["id"]
    ).first()


    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # ---------- SAVE FILE ----------
    upload_dir = "uploads/resumes"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{application_id}.pdf"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------- EXTRACT TEXT ----------
    resume_text = extract_text_from_pdf(file_path)

    # ---------- GET JOB ----------
    job = db.query(JobListing).filter(
        JobListing.id == application.job_id
    ).first()

    # ---------- TF-IDF SCORE ----------
    tfidf_score = calculate_resume_score(
        resume_text,
        job.description or ""
    )

    # ---------- AI SCORE ----------
    ai_result = analyze_resume_with_ai(
        resume_text=resume_text,
        job_description=job.description or ""
    )

    ai_score = ai_result["score"]

    # ---------- FINAL SCORE ----------
    final_score = int((0.4 * tfidf_score) + (0.6 * ai_score))

    # ---------- STATUS ----------
    if job.min_score_required and final_score >= job.min_score_required:
        application.status = "shortlisted"
    else:
        application.status = "rejected"

    application.resume_url = file_path
    application.resume_score = final_score

    db.commit()

    return {
        "message": "Resume uploaded and analyzed",
        "tfidf_score": tfidf_score,
        "ai_score": ai_score,
        "final_score": final_score,
        "status": application.status
    }
