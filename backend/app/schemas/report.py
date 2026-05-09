from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReportBase(BaseModel):
    seller_id: int
    report_type: str
    description: str
    amount_lost: Optional[float] = None
    evidence_url: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class ReportResponse(ReportBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True