from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
import database, models
from routes.auth import get_current_user
from services.nlp_service import calculate_similarity, extract_missing_skills

router = APIRouter()

@router.post("/analyze")
def analyze_job_fit(
    resume_id: int = Form(...),
    job_description_text: str = Form(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id, models.Resume.owner_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    score = calculate_similarity(resume.content, job_description_text)
    missing = extract_missing_skills(resume.content, job_description_text)
    
    feedback = f"Your resume has a {score}% match for this job fit test. Missing skills: {', '.join(missing) if missing else 'None detected'}."
    
    analysis = models.JobFitAnalysis(
        user_id=current_user.id,
        resume_id=resume.id,
        match_score=score,
        feedback=feedback
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return {"message": "Analysis complete", "match_score": score, "missing_skills": missing, "feedback": feedback, "analysis_id": analysis.id}
