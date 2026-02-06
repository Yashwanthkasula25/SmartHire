from sqlalchemy import Column, Integer, String, Text, DateTime , ForeignKey 
from sqlalchemy.sql import func
from ..db.database import Base
from sqlalchemy.orm import relationship



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


