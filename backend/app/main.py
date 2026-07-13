from fastapi import FastAPI
from app.routers import resume

app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0.0"
)

app.include_router(resume.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer API"
    }