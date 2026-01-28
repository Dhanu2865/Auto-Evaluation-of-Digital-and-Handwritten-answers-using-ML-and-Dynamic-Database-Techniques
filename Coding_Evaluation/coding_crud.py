from coding.coding_models import (
    CodingQuestion, TestCase, CodeSubmission, CodingResult
)

def get_coding_question(db, question_id):
    return db.query(CodingQuestion).filter_by(id=question_id).first()

def get_test_cases(db, question_id):
    return db.query(TestCase).filter_by(question_id=question_id).all()

def save_code_submission(db, question_id, code):
    submission = CodeSubmission(
        question_id=question_id,
        student_code=code
    )
    db.add(submission)
    db.flush()
    return submission

def save_coding_result(db, submission_id, passed, total, marks):
    result = CodingResult(
        submission_id=submission_id,
        passed_cases=passed,
        total_cases=total,
        marks=marks
    )
    db.add(result)
