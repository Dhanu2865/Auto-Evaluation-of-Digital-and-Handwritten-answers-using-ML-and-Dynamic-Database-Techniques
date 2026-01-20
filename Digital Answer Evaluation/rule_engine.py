import re

def rule_based_score(student_answer: str, key_concepts: str) -> float:
    if not key_concepts:
        return 0.0

    student_text = student_answer.lower()

    concepts = [
        c.strip().lower()
        for c in key_concepts.split(",")
        if c.strip()
    ]

    if not concepts:
        return 0.0

    hits = 0
    for c in concepts:
        if c in student_text:  
            hits += 1

    return hits / len(concepts)