from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.seller import Seller
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportResponse
from app.services.evidence_builder import build_report_evidence_text
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore

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
    
    
    
@router.get("/{report_id}/evidence-text")
def get_report_evidence_text(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    seller = db.query(Seller).filter(Seller.id == report.seller_id).first()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    evidence_text = build_report_evidence_text(seller, report)

    return {
        "report_id": report.id,
        "seller_id": seller.id,
        "evidence_text": evidence_text
    }
    
@router.post("/{report_id}/ingest")
def ingest_report_into_vector_store(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    seller = db.query(Seller).filter(Seller.id == report.seller_id).first()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    evidence_text = build_report_evidence_text(seller, report)

    embedding_service = EmbeddingService()
    vector_store = VectorStore()

    embedding = embedding_service.embed_text(evidence_text)

    metadata = {
        "report_id": report.id,
        "seller_id": seller.id,
        "seller_name": seller.seller_name,
        "report_type": report.report_type,
        "status": report.status,
        "amount_lost": report.amount_lost,
        "evidence_text": evidence_text,
    }

    vector_store.add_document(embedding, metadata)

    return {
        "message": "Report ingested successfully",
        "report_id": report.id,
        "seller_id": seller.id
    }
    
    
@router.get("/rag/search")
def search_report_evidence(query: str, top_k: int = 5):
    embedding_service = EmbeddingService()
    vector_store = VectorStore()

    query_embedding = embedding_service.embed_text(query)

    results = vector_store.search(query_embedding, top_k=top_k)

    return {
        "query": query,
        "top_k": top_k,
        "results": results
    }