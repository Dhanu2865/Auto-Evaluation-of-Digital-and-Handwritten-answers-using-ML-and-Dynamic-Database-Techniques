from models import ReferenceAnswer

def request_reference_promotion(db, question_id, student_answer, similarity, threshold=0.85):
    if similarity >= threshold:
        ref = ReferenceAnswer(
            question_id=question_id,
            answer_text=student_answer,
            key_concepts="",
            source_type="student"
        )
        db.add(ref)
        db.commit()
        return True
    return False