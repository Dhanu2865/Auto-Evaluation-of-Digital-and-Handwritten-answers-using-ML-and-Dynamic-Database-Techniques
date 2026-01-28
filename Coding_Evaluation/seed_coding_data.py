from database import Base, engine, SessionLocal
from coding.coding_models import CodingQuestion, TestCase

Base.metadata.create_all(bind=engine)
db = SessionLocal()

question = CodingQuestion(
    topic="Programming",
    problem_statement="Write a program to check whether a number is prime.",
    max_marks=10
)
db.add(question)
db.commit()
db.refresh(question)

test_cases = [
    ("5", "True"),
    ("4", "False"),
    ("2", "True"),
    ("1", "False"),
    ("9", "False")
]

for inp, out in test_cases:
    db.add(TestCase(
        question_id=question.id,
        input_data=inp,
        expected_output=out
    ))

db.commit()
db.close()

print("✅ Coding question seeded")
