from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..models.job import JobListing
from ..schemas.job import JobCreate, JobResponse
from ..core.auth import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# POST /jobs/ → Recruiter Creates Job
@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # ✅ Allow only recruiters
    if current_user["role"].lower() != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Only recruiters can create jobs"
        )

    job = JobListing(
        recruiter_id=current_user["id"],
        **job_data.model_dump()
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


# GET /jobs/ → List All Jobs
@router.get("/", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(JobListing).all()




# GET /jobs/my — Recruiter’s Jobs
@router.get("/my", response_model=list[JobResponse])
def get_my_jobs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # ✅ Only recruiter allowed
    if current_user["role"].lower() != "recruiter":
        raise HTTPException(
            status_code=403,
            detail="Only recruiters can view their jobs"
        )

    jobs = db.query(JobListing).filter(
        JobListing.recruiter_id == current_user["id"]
    ).all()

    return jobs

# GET /jobs/{id} → Job Details
@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobListing).filter(
        JobListing.id == job_id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
