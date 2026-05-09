from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    seller_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, nullable=True)
    business_name = Column(String, nullable=True)
    social_handle = Column(String, nullable=True)
    bank_account_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship("Report", back_populates="seller")