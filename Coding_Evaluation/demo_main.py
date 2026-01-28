from database import SessionLocal
from coding.coding_crud import (
    get_coding_question,
    get_test_cases,
    save_code_submission,
    save_coding_result
)
from coding.coding_evaluator import evaluate_code

db = SessionLocal()

question = get_coding_question(db, 1)
print("CODING QUESTION:")
print(question.problem_statement)

print("\nPlease write your code in 'student_code.py' and save it.")
input("Press ENTER after saving the file...")

# 🔹 Read code from file
with open("student_code.py", "r") as f:
    student_code = f.read()

test_cases = get_test_cases(db, question.id)

submission = save_code_submission(db, question.id, student_code)

passed, total, marks = evaluate_code(
    student_code,
    test_cases,
    question.max_marks
)

save_coding_result(db, submission.id, passed, total, marks)
db.commit()

print("\nRESULT:")
print(f"Passed Test Cases: {passed}/{total}")
print(f"Marks: {marks}/{question.max_marks}")

db.close()
