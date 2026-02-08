from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from crud import get_pending_reviews, update_review_status
from schemas import ReviewAction

from models import EvaluationResult, StudentSubmission, Question, ReferenceAnswer
router = APIRouter(prefix="/admin", tags=["Admin"])
from pydantic import BaseModel

class ReviewAction(BaseModel):
    status: str


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/review/{result_id}")
def update_review_status(
    result_id: int,
    action: ReviewAction,
    db: Session = Depends(get_db)
):
    result = db.query(EvaluationResult).filter(
        EvaluationResult.id == result_id
    ).first()

    if not result:
        return {"message": "Result not found"}

    if action.status not in ["APPROVED", "REJECTED"]:
        return {"message": "Invalid status"}

    result.status = action.status
    db.commit()

    return {"message": f"Review {action.status.lower()} successfully"}

from models import StudentSubmission

@router.get("/pending")
def fetch_pending_reviews(db: Session = Depends(get_db)):
    results = get_pending_reviews(db)

    response = []

    for r in results:
        submission = db.query(StudentSubmission).filter(
            StudentSubmission.id == r.submission_id
        ).first()

        response.append({
            "result_id": r.id,
            "submission_id": r.submission_id,
            "student_id": submission.student_id if submission else "UNKNOWN",
            "percentage": r.percentage
        })

    return response

@router.get("/review/{result_id}")
def get_review_details(result_id: int, db: Session = Depends(get_db)):
    result = db.query(EvaluationResult).filter(
        EvaluationResult.id == result_id
    ).first()

    submission = db.query(StudentSubmission).filter(
        StudentSubmission.id == result.submission_id
    ).first()

    question = db.query(Question).filter(
        Question.id == submission.question_id
    ).first()

    reference = db.query(ReferenceAnswer).filter(
        ReferenceAnswer.question_id == question.id,
        ReferenceAnswer.source_type == "teacher"
    ).first()

    return {
        "question": question.question_text,
        "student_answer": submission.answer_text,
        "teacher_answer": reference.answer_text,
        "percentage": result.percentage,
        "status": result.status
    }
