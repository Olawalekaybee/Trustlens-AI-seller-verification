from fastapi import FastAPI

app = FastAPI(
    title="TrustLens API",
    description="AI-powered seller verification and fraud risk intelligence platform",
    version="1.0.0",
)


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