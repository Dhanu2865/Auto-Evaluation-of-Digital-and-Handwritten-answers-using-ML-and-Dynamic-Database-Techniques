from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from database import SessionLocal
from crud import (
    get_topics,
    get_questions_by_topics,
    get_reference_answers,
    save_submission,
    save_result,
    generate_student_id
)

from schemas import (
    TopicResponse,
    QuestionResponse,
    SubmitTestRequest
)

from preprocessing import preprocess_text
from semantic_engine import sentence_level_similarity
from rule_engine import rule_based_score
from scoring_engine import calculate_final_percentage
from explainable_ai import generate_explanation
from gemini_explainer import generate_gemini_explanation
from reference_manager import request_reference_promotion

from admin_routes import router as admin_router
from models import Question


# --------------------------------------------------
# APP INITIALIZATION
# --------------------------------------------------

app = FastAPI(title="Automated Answer Evaluation System")

app.include_router(admin_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


# --------------------------------------------------
# DATABASE DEPENDENCY
# --------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# AI EXPLANATION FORMATTER (MUST COME FIRST)
# --------------------------------------------------

def format_ai_explanation(text: str):
    if not text:
        return {
            "correct": "",
            "missing": "",
            "improve": ""
        }

    sections = {
        "correct": "",
        "missing": "",
        "improve": ""
    }

    lower = text.lower()

    try:
        if "what parts of the student answer are correct" in lower:
            sections["correct"] = text.split("1.")[1].split("2.")[0].strip()

        if "what important points are missing" in lower:
            sections["missing"] = text.split("2.")[1].split("3.")[0].strip()

        if "how the answer can be improved" in lower:
            sections["improve"] = text.split("3.")[1].strip()
    except Exception:
        # fallback if Gemini response format changes
        sections["improve"] = text

    return sections


# --------------------------------------------------
# STUDENT APIs
# --------------------------------------------------

@app.get("/topics", response_model=list[TopicResponse])
def fetch_topics(db: Session = Depends(get_db)):
    return get_topics(db)


@app.get("/topics/{topic_id}/questions", response_model=list[QuestionResponse])
def fetch_questions(topic_id: int, db: Session = Depends(get_db)):
    return get_questions_by_topics(db, topic_id)


@app.post("/submit-test")
def submit_test(payload: SubmitTestRequest, db: Session = Depends(get_db)):

    # Generate ONE student ID per test attempt
    student_id = generate_student_id(db)

    final_report = []
    total_marks = 0.0
    total_max_marks = 0

    for item in payload.answers:
        student_answer = item.answer_text
        clean_student = preprocess_text(student_answer)

        references = get_reference_answers(db, item.question_id)

        # ---------- Semantic similarity ----------
        ml_score = 0.0
        for ref in references:
            clean_ref = preprocess_text(ref.answer_text)
            score = sentence_level_similarity(clean_student, clean_ref)
            ml_score = max(ml_score, score)

        ml_score = float(ml_score)  # JSON-safe

        teacher_ref = next(ref for ref in references if ref.source_type == "teacher")

        rule_score = rule_based_score(
            clean_student,
            teacher_ref.key_concepts
        )

        # ---------- Evaluation ----------
        if ml_score < 0.45 or (rule_score == 0.0 and ml_score < 0.6):
            final_score = ml_score
            answer_type = "Irrelevant Answer"
            status = "AUTO_EVALUATED"
            promote = False
            rule_explanation = "Answer meaning does not align with expected concepts."
            ai_feedback = {
                "correct": "",
                "missing": "Answer is irrelevant to the question.",
                "improve": "Please answer according to the given question."
            }
        else:
            final_score, _ = calculate_final_percentage(ml_score, rule_score)
            final_score = float(final_score)

            if ml_score >= 0.98:
                final_score = 1.0
                answer_type = "Perfect Answer"
                status = "PENDING"
                promote = True
            elif final_score >= 0.9 and rule_score >= 0.8:
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

            raw_ai = generate_gemini_explanation(
                teacher_ref.answer_text,
                student_answer
            )

            ai_feedback = format_ai_explanation(raw_ai)

        # ---------- Save submission ----------
        submission = save_submission(
            db,
            item.question_id,
            student_answer,
            student_id
        )

        save_result(
            db=db,
            submission_id=submission.id,
            similarity_score=ml_score,
            percentage=round(final_score * 100, 2),
            explanation=rule_explanation,
            answer_type=answer_type,
            status=status
        )

        if promote:
            request_reference_promotion(
                db,
                item.question_id,
                student_answer,
                ml_score
            )

        question = db.query(Question).filter(
            Question.id == item.question_id
        ).first()

        marks = round(final_score * question.max_marks, 2)

        total_marks += marks
        total_max_marks += question.max_marks

        # ---------- AI score formatting ----------
        ai_percentage = round(ml_score * 100, 2)
        ai_marks = round(ml_score * question.max_marks, 2)

        final_report.append({
            "question": question.question_text,
            "marks": marks,
            "max_marks": question.max_marks,
            "category": answer_type,
            "ai_percentage": ai_percentage,
            "ai_marks": ai_marks,
            "reference_answer": teacher_ref.answer_text,
            "rule_explanation": rule_explanation,
            "ai_feedback": ai_feedback
        })

    overall_percentage = round((total_marks / total_max_marks) * 100, 2)
    result_status = "PASS" if overall_percentage >= 40 else "FAIL"

    return {
        "student_id": student_id,
        "questions": final_report,
        "total_marks": round(total_marks, 2),
        "total_max_marks": total_max_marks,
        "overall_percentage": overall_percentage,
        "result_status": result_status
    }


# --------------------------------------------------
# HTML ROUTES (MUST BE LAST)
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/{page_name}", response_class=HTMLResponse)
def serve_pages(page_name: str):
    file_path = f"templates/{page_name}"
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("<h3>Page not found</h3>", status_code=404)
