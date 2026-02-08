from models import (
    Topic,
    Question,
    ReferenceAnswer,
    StudentSubmission,
    EvaluationResult
)


# ------------------ STUDENT ------------------

def get_topics(db):
    return db.query(Topic).all()


def get_questions_by_topics(db, topic_id):
    return db.query(Question).filter(
        Question.topic_id == topic_id
    ).all()


def get_reference_answers(db, question_id):
    return db.query(ReferenceAnswer).filter(
        ReferenceAnswer.question_id == question_id
    ).all()


def save_submission(db, question_id, answer_text, student_id=None):
    submission = StudentSubmission(
        question_id=question_id,
        answer_text=answer_text,
        student_id=student_id
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def save_result(
    db,
    submission_id,
    similarity_score,
    percentage,
    explanation,
    answer_type,
    status="PENDING"
):
    result = EvaluationResult(
        submission_id=submission_id,
        similarity_score=similarity_score,
        percentage=percentage,
        explanation=explanation,
        answer_type=answer_type,
        status=status
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_student_results(db, student_id):
    return (
        db.query(EvaluationResult)
        .join(StudentSubmission,
              StudentSubmission.id == EvaluationResult.submission_id)
        .filter(StudentSubmission.student_id == student_id)
        .all()
    )


# ------------------ ADMIN ------------------

def get_pending_reviews(db):
    return db.query(EvaluationResult).filter(
        EvaluationResult.status == "PENDING",
        EvaluationResult.answer_type == "Perfect Answer"
    ).all()

import re
from models import StudentSubmission

def generate_student_id(db):
    """
    Generates a new student ID in the form STUDENT_1, STUDENT_2, ...
    Safely ignores malformed or old student IDs.
    """

    submissions = db.query(StudentSubmission.student_id).all()

    max_id = 0

    for (sid,) in submissions:
        if not sid:
            continue

        match = re.match(r"STUDENT_(\d+)", sid)
        if match:
            num = int(match.group(1))
            max_id = max(max_id, num)

    return f"STUDENT_{max_id + 1}"



def update_review_status(db, result_id, status):
    result = db.query(EvaluationResult).get(result_id)
    result.status = status
    db.commit()
    return result
