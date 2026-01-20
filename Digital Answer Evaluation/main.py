from database import SessionLocal
from crud import (
    get_topics,
    get_questions_by_topics,
    get_reference_answers,
    save_submission,
    save_result
)
from preprocessing import preprocess_text
from semantic_engine import sentence_level_similarity
from rule_engine import rule_based_score
from scoring_engine import calculate_final_percentage
from explainable_ai import generate_explanation
from reference_manager import request_reference_promotion
from gemini_explainer import generate_gemini_explanation


def main():
    db = SessionLocal()
    final_report = []

    topics = get_topics(db)
    print("Available Topics:")
    for t in topics:
        print(f"{t.id}. {t.name}")

    topic_id = int(input("Choose topic ID: "))

    questions = get_questions_by_topics(db, topic_id)
    print(f"\nThis topic has {len(questions)} questions.\n")

    total_possible_marks = sum(q.max_marks for q in questions)

    for idx, question in enumerate(questions, start=1):
        print(f"\nQuestion {idx}: {question.question_text}")

        student_answer = input("\nEnter your answer:\n")
        clean_student = preprocess_text(student_answer)

        references = get_reference_answers(db, question.id)

        ml_score = 0.0
        for ref in references:
            clean_ref = preprocess_text(ref.answer_text)
            ml_score = max(ml_score, sentence_level_similarity(clean_student, clean_ref))

        teacher_ref = next(ref for ref in references if ref.source_type == "teacher")
        rule_score = rule_based_score(clean_student, teacher_ref.key_concepts)

        if ml_score < 0.45:
            final_score = ml_score
            answer_type = "Irrelevant Answer"
            rule_explanation = "Answer meaning does not align with expected concepts."
            gemini_explanation = "Answer is irrelevant; detailed AI explanation is not applicable."
            status = "AUTO_EVALUATED"
            promote = False

        elif rule_score == 0.0 and ml_score < 0.6:
            final_score = ml_score
            answer_type = "Irrelevant Answer"
            rule_explanation = "Key concepts are missing and semantic relevance is low."
            gemini_explanation = "Answer is irrelevant; detailed AI explanation is not applicable."
            status = "AUTO_EVALUATED"
            promote = False

        else:
            final_score, percentage = calculate_final_percentage(ml_score, rule_score)

            if final_score >= 0.9 and rule_score >= 0.8:
                answer_type = "Perfect Answer"
                status = "PENDING"
                promote = True
            elif final_score >= 0.6:
                answer_type = "Relevant Answer"
                status = "AUTO_EVALUATED"
                promote = False
            else:
                answer_type = "Irrelevant Answer"
                status = "AUTO_EVALUATED"
                promote = False

            rule_explanation = generate_explanation(ml_score, rule_score)

            if answer_type in ["Perfect Answer", "Relevant Answer"]:
                gemini_explanation = generate_gemini_explanation(
                    teacher_ref.answer_text,
                    student_answer
                )
            else:
                gemini_explanation = "Answer is irrelevant; detailed AI explanation is not applicable."

        marks = round(final_score * question.max_marks, 2)
        marks = min(marks, question.max_marks)

        percentage = round(final_score * 100, 2)

        submission = save_submission(db, question.id, student_answer)

        save_result(
            db=db,
            submission_id=submission.id,
            similarity_score=ml_score,
            percentage=percentage,
            explanation=rule_explanation,
            answer_type=answer_type,
            status=status
        )

        db.commit()   

        if promote:
            request_reference_promotion(
                db,
                question.id,
                student_answer,
                ml_score
            )

        final_report.append({
            "question": question.question_text,
            "answer": student_answer,
            "percentage": percentage,
            "marks": marks,
            "max_marks": question.max_marks,
            "category": answer_type,
            "rule_explanation": rule_explanation,
            "gemini_explanation": gemini_explanation
        })

        print("\nAnswer saved. Moving to next question...")
        print("-" * 50)

    print("\n================ FINAL RESULT SUMMARY ================\n")

    total_marks = 0.0
    for i, item in enumerate(final_report, start=1):
        print(f"Question {i}: {item['question']}")
        print(f"Your Answer: {item['answer']}")
        print(f"Score: {item['percentage']:.2f}%")
        print(f"Marks: {item['marks']:.2f}/{item['max_marks']}")
        print(f"Category: {item['category']}")
        print(f"Rule-Based Explanation: {item['rule_explanation']}")
        print(f"AI Explanation (Gemini): {item['gemini_explanation']}")
        print("-" * 60)
        total_marks += item["marks"]

    total_marks = round(total_marks, 2)
    overall_percentage = round((total_marks / total_possible_marks) * 100, 2)

    result_status = "PASS" if overall_percentage >= 40 else "FAIL"

    print("\n================ OVERALL RESULT ================\n")
    print(f"Total Marks: {total_marks:.2f}/{total_possible_marks}")
    print(f"Overall Percentage: {overall_percentage:.2f}%")
    print(f"Final Result: {result_status}")
    print("\nOnly perfect answers were sent for teacher review.")

    db.commit()
    db.close()


if __name__ == "__main__":
    main()