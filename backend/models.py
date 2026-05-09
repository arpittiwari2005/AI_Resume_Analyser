from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # 'student' or 'admin'
    
    resumes = relationship("Resume", back_populates="owner")

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))

    resumes = relationship("Resume", back_populates="job")

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(Text) # Extracted text
    similarity_score = Column(Float, default=0.0)
    missing_skills = Column(Text) # Comma-separated or JSON string
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))

    owner = relationship("User", back_populates="resumes")
    job = relationship("JobDescription", back_populates="resumes")

class CoverLetter(Base):
    __tablename__ = "cover_letters"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    job_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ResumeVersion(Base):
    __tablename__ = "resume_versions"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    content = Column(Text)
    version_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MockInterview(Base):
    __tablename__ = "mock_interviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    overall_score = Column(Float)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class JobFitAnalysis(Base):
    __tablename__ = "job_fit_analyses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    match_score = Column(Float)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)
