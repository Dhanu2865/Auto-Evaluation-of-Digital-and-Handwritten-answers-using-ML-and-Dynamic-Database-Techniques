from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base

class CodingQuestion(Base):
    __tablename__ = "coding_questions"

    id = Column(Integer, primary_key=True)
    topic = Column(String(100))
    problem_statement = Column(Text)
    max_marks = Column(Integer, default=10)
    language = Column(String(20), default="python")


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("coding_questions.id"))
    input_data = Column(Text)
    expected_output = Column(Text)


class CodeSubmission(Base):
    __tablename__ = "code_submissions"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    student_code = Column(Text)


class CodingResult(Base):
    __tablename__ = "coding_results"

    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer)
    passed_cases = Column(Integer)
    total_cases = Column(Integer)
    marks = Column(Integer)
