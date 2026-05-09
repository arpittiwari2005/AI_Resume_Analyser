from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
import database, models
from routes.auth import get_current_user

router = APIRouter()

@router.post("/generate")
def generate_cover_letter(
    resume_id: int = Form(...),
    job_id: int = Form(None),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id, models.Resume.owner_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Mocking Cover Letter Generation
    content = f"Dear Hiring Manager,\n\nI am writing to express my interest in the role. With my background highlighted in {resume.filename}, I am confident in my skills and abilities.\n\nSincerely,\n{current_user.email}"
    
    cl = models.CoverLetter(user_id=current_user.id, resume_id=resume.id, job_id=job_id, content=content)
    db.add(cl)
    db.commit()
    db.refresh(cl)
    return {"message": "Cover letter generated", "cover_letter_id": cl.id, "content": content}
