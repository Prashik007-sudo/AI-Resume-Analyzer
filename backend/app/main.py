from fastapi import FastAPI
from app.routers import resume
from app.routers.jd import router as jd_router

app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0.0"
)

app.include_router(resume.router)
app.include_router(jd_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer API"
    }