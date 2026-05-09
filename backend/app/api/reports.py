from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.seller import Seller
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportResponse

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/", response_model=ReportResponse)
def create_report(report_data: ReportCreate, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.id == report_data.seller_id).first()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    report = Report(**report_data.model_dump())

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


@router.get("/seller/{seller_id}", response_model=list[ReportResponse])
def get_reports_by_seller(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    return db.query(Report).filter(
        Report.seller_id == seller_id
    ).order_by(Report.created_at.desc()).all()