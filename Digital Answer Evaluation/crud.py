from models import Topic, Question, ReferenceAnswer, StudentSubmission, EvaluationResult

def get_topics(db):
    return db.query(Topic).all()

def get_questions_by_topics(db, topic_id):
    return db.query(Question).filter(Question.topic_id == topic_id).all()

def get_reference_answers(db, question_id):
    return db.query(ReferenceAnswer).filter(
        ReferenceAnswer.question_id == question_id
    ).all()

def save_submission(db, question_id, answer_text):
    submission = StudentSubmission(
        question_id=question_id,
        answer_text=answer_text
    )
    db.add(submission)
    db.commit()     
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