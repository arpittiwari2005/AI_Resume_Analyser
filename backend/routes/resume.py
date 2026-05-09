from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List

import database
import models
import schemas
from routes.auth import get_current_user
from services.nlp_service import extract_text_from_pdf, extract_text_from_docx, calculate_similarity, extract_missing_skills
import json

router = APIRouter()

@router.post("/upload")
async def upload_resume(
    job_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != 'student':
        raise HTTPException(status_code=403, detail="Only students can upload resumes")
        
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")

    content = await file.read()
    
    text = ""
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(content)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX formats are supported")

    # Analyze similarity
    score = calculate_similarity(text, job.description)
    missing_skills = extract_missing_skills(text, job.description)

    # Save logic
    resume = models.Resume(
        filename=file.filename,
        content=text,
        similarity_score=score,
        missing_skills=json.dumps(missing_skills),
        owner_id=current_user.id,
        job_id=job.id
    )
    
    db.add(resume)
    db.commit()
    db.refresh(resume)

    version = models.ResumeVersion(
        resume_id=resume.id,
        content=text,
        version_number=1
    )
    db.add(version)
    db.commit()

    return {"message": "Resume uploaded successfully", "score": score, "missing_skills": missing_skills}

@router.post("/jobs")
def create_job(
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Only admins can post job descriptions")
        
    new_job = models.JobDescription(
        title=title,
        description=description,
        created_by=current_user.id
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": "Job description created", "job_id": new_job.id}

@router.get("/jobs")
def get_jobs(db: Session = Depends(database.get_db)):
    return db.query(models.JobDescription).all()

@router.get("/jobs/{job_id}/resumes")
def get_job_resumes(
    job_id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Only admins can view ranked resumes")
        
    resumes = db.query(models.Resume, models.User.email).join(models.User).filter(models.Resume.job_id == job_id).order_by(models.Resume.similarity_score.desc()).all()
    
    results = []
    for resume, email in resumes:
        results.append({
            "id": resume.id,
            "student_email": email,
            "filename": resume.filename,
            "score": resume.similarity_score,
            "missing_skills": json.loads(resume.missing_skills) if resume.missing_skills else []
        })
    return results

@router.get("/my-resumes")
def get_my_resumes(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != 'student':
        raise HTTPException(status_code=403, detail="Only students have their own resumes")
        
    resumes = db.query(models.Resume, models.JobDescription.title).join(models.JobDescription).filter(models.Resume.owner_id == current_user.id).all()
    
    results = []
    for resume, jd_title in resumes:
        results.append({
            "id": resume.id,
            "job_title": jd_title,
            "filename": resume.filename,
            "score": resume.similarity_score,
            "missing_skills": json.loads(resume.missing_skills) if resume.missing_skills else []
        })
    return results
