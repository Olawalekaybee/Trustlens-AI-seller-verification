from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)

    report_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    amount_lost = Column(Float, nullable=True)
    evidence_url = Column(String, nullable=True)
    status = Column(String, default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)

    seller = relationship("Seller", back_populates="reports")