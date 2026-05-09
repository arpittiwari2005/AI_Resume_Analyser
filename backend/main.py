from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
import routes.auth
import routes.resume
import routes.interview
import routes.cover_letter
import routes.job_fit
# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Analyzer API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(routes.auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(routes.resume.router, prefix="/api/resume", tags=["resume"])
app.include_router(routes.interview.router, prefix="/api/interview", tags=["interview"])
app.include_router(routes.cover_letter.router, prefix="/api/cover-letter", tags=["cover-letter"])
app.include_router(routes.job_fit.router, prefix="/api/job-fit", tags=["job-fit"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Resume Analyzer API"}
