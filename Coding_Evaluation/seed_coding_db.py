from database import Base, engine, SessionLocal
from coding.coding_models import CodingQuestion, CodingTestCase

# -------- CREATE TABLES --------
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Prevent duplicate seeding
existing = db.query(CodingQuestion).first()
if existing:
    print("Coding tables already seeded.")
    db.close()
    exit()

# -------- INSERT QUESTION --------
question = CodingQuestion(
    topic="Programming Basics",
    problem_statement="Write a program to check whether a number is prime.",
    max_marks=10,
    language="multi"
)

db.add(question)
db.commit()
db.refresh(question)

# -------- INSERT TEST CASES --------
test_cases = [
    CodingTestCase(question_id=question.id, input_data="7", expected_output="Prime"),
    CodingTestCase(question_id=question.id, input_data="10", expected_output="Not Prime"),
    CodingTestCase(question_id=question.id, input_data="2", expected_output="Prime"),
    CodingTestCase(question_id=question.id, input_data="1", expected_output="Not Prime")
]

db.add_all(test_cases)
db.commit()
db.close()

print("✅ Coding database seeded successfully.")
