from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
import database
import models
import schemas
from routes.auth import get_current_user
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

# Helper to load JSON questions
def load_questions():
    file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'interview_questions.json'))
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.get("/questions")
def get_interview_questions(resume_id: int = None, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    questions_data = load_questions()
    
    # Default to generic Software Engineer questions
    fallback_questions = questions_data.get("Software Engineer", [])

    if not resume_id:
        return fallback_questions

    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not resume:
        return fallback_questions
        
    job = db.query(models.JobDescription).filter(models.JobDescription.id == resume.job_id).first()
    if not job:
        return fallback_questions
        
    title_lower = job.title.lower()
    
    # Find matching role structure conceptually
    for role, qs in questions_data.items():
        if role.lower() in title_lower or title_lower in role.lower():
            return qs
            
    return fallback_questions

@router.post("/evaluate")
def evaluate_interview_response(
    question_id: int = Form(...),
    user_answer: str = Form(...),
    expected_answer: str = Form(...),
    resume_id: int = Form(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verify resume belongs to user
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not resume or resume.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # AI Comparison Logic using TF-IDF cosine similarity
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([expected_answer, user_answer])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        score = int(similarity * 100)
    except Exception as e:
        score = 50 # Default fallback
        
    # Generate generic AI feedback based on score
    if score >= 60:
        base_feedback = "Great response! You hit the main points nicely and provided good context."
    elif score >= 30:
        base_feedback = "Not bad, but you could elaborate more and align closer to standard industry practices."
    else:
        base_feedback = "I think you missed the core of the question. Try to focus on the key concepts mentioned."
        
    summary = f"Summary of your answer: '{user_answer[:70]}...' " if len(user_answer) > 70 else f"Summary of your answer: '{user_answer}'. "
    
    # Extract keywords from expected_answer for key points
    import re
    words = re.findall(r'\b\w+\b', expected_answer.lower())
    stop_words = {"the", "and", "a", "to", "of", "in", "i", "is", "that", "it", "on", "you", "this", "for", "but", "with", "are", "have", "be", "at", "or", "as", "was", "so", "if", "out", "not"}
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    unique_keywords = list(dict.fromkeys(keywords))[:5]
    focus_points = ", ".join(unique_keywords)
    
    full_feedback = f"{summary}\n\n{base_feedback}\n\nKey points to focus on: {focus_points}."
    
    # Log to MockInterview DB table
    interview_record = models.MockInterview(
        user_id=current_user.id,
        overall_score=score,
        feedback=f"Q{question_id}: {full_feedback}"
    )
    db.add(interview_record)
    db.commit()
    db.refresh(interview_record)
        
    return {"score": score, "feedback": full_feedback, "interview_id": interview_record.id}
