from pydantic import BaseModel
from typing import List, Optional


# ----------- STUDENT SCHEMAS -----------

class AnswerInput(BaseModel):
    question_id: int
    answer_text: str


class SubmitTestRequest(BaseModel):
    student_id: str
    topic_id: int
    answers: List[AnswerInput]


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    max_marks: int


class TopicResponse(BaseModel):
    id: int
    name: str


class ResultResponse(BaseModel):
    question: str
    percentage: float
    marks: float
    max_marks: int
    category: str
    rule_explanation: str
    gemini_explanation: str


# ----------- ADMIN SCHEMAS -----------

class ReviewAction(BaseModel):
    status: str  # APPROVED / REJECTED
