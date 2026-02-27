from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..db.database import Base
from sqlalchemy.orm import relationship


class Interview(Base):
    __tablename__ = "interview"

    id = Column(Integer, primary_key=True, index=True)

    candidate_application_id = Column(
        Integer,
        ForeignKey("candidate_application.id", ondelete="CASCADE")
    )

    audio_url = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)
    duration = Column(Integer, nullable=True)

    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)

    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    recommendation = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())

    application = relationship(
        "CandidateApplication",
        backref="interview"
    )
