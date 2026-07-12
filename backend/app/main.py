from fastapi import FastAPI

app = FastAPI(
    title="AI Resume Analyzer API",
    description="Backend API for the AI Resume Analyzer project",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer API",
        "status": "Running"
    }