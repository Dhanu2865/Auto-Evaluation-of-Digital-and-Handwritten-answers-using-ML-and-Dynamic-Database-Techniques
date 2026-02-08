from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from database import Base
from datetime import datetime


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    question_text = Column(Text)
    max_marks = Column(Integer)


class ReferenceAnswer(Base):
    __tablename__ = "reference_answers"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(Text)
    key_concepts = Column(Text)
    source_type = Column(String, default="teacher")  # teacher / student


class StudentSubmission(Base):
    __tablename__ = "student_submissions"
    id = Column(Integer, primary_key=True)
    student_id = Column(String, nullable=True)
    question_id = Column(Integer)
    answer_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer)
    similarity_score = Column(Float)
    percentage = Column(Float)
    explanation = Column(Text)
    answer_type = Column(String)
    status = Column(String, default="PENDING")  # PENDING / APPROVED / REJECTED
