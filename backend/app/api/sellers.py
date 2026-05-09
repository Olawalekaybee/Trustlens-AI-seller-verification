from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.seller import Seller
from app.schemas.seller import SellerCreate, SellerResponse

router = APIRouter(
    prefix="/sellers",
    tags=["Sellers"]
)


@router.post("/", response_model=SellerResponse)
def create_seller(seller_data: SellerCreate, db: Session = Depends(get_db)):
    existing_seller = None

    if seller_data.phone_number:
        existing_seller = db.query(Seller).filter(
            Seller.phone_number == seller_data.phone_number
        ).first()

    if existing_seller:
        raise HTTPException(
            status_code=400,
            detail="Seller with this phone number already exists"
        )

    seller = Seller(**seller_data.model_dump())

    db.add(seller)
    db.commit()
    db.refresh(seller)

    return seller


@router.get("/", response_model=list[SellerResponse])
def get_sellers(db: Session = Depends(get_db)):
    return db.query(Seller).order_by(Seller.created_at.desc()).all()


@router.get("/{seller_id}", response_model=SellerResponse)
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(Seller).filter(Seller.id == seller_id).first()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    return seller