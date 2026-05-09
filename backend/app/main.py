from fastapi import FastAPI

from app.db.database import Base, engine
from app.models import seller, report
from app.api import sellers, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TrustLens API",
    description="AI-powered seller verification and fraud risk intelligence platform",
    version="1.0.0",
)


app.include_router(sellers.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to TrustLens API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "trustlens-api"
    }