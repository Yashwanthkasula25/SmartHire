from sqlalchemy import Column, Integer, String, Text, DateTime , ForeignKey 
from sqlalchemy.sql import func
from ..db.database import Base
from sqlalchemy.orm import relationship



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
