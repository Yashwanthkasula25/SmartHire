from sqlalchemy import Column, Integer, String, Text, DateTime , ForeignKey 
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    full_name = Column(String(100))
    company_name = Column(String(150))
    experience_years = Column(Integer)
    skills = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="profile")


class JobListing(Base):
    __tablename__ = "job_listing"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(150), nullable=False)
    role = Column(String(100))
    description = Column(Text)
    package = Column(String(50))
    location = Column(String(100))
    mode = Column(String(20))
    experience_required = Column(Integer)
    status = Column(String(20), default="open")
    min_score_required = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recruiter = relationship("User", backref="job_listings")


class CandidateApplication(Base):
    __tablename__ = "candidate_application"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    job_id = Column(Integer, ForeignKey("job_listing.id", ondelete="CASCADE"))
    resume_url = Column(Text)
    resume_score = Column(Integer)
    voice_score = Column(Integer)
    final_score = Column(Integer)
    status = Column(String(30), default="applied")
    interview_completed = Column(Integer, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="applications")
    job = relationship("JobListing", backref="applications")


class Interview(Base):
    __tablename__ = "interview"

    id = Column(Integer, primary_key=True, index=True)
    candidate_application_id = Column(
        Integer,
        ForeignKey("candidate_application.id", ondelete="CASCADE"),
        unique=True
    )
    audio_url = Column(Text)
    transcript = Column(Text)
    duration = Column(Integer)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)

    application = relationship("CandidateApplication", backref="interview")
