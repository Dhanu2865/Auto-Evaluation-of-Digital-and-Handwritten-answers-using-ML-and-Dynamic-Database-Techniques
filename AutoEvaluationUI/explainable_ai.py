def generate_explanation(ml_score, rule_score):
    reasons = []

    if ml_score >= 0.8:
        reasons.append("Answer meaning closely matches reference answer.")
    elif ml_score >= 0.5:
        reasons.append("Answer is partially relevant to the question.")
    else:
        reasons.append("Answer meaning does not align with expected concepts.")

    if rule_score == 1.0:
        reasons.append("All key concepts are covered.")
    elif rule_score >= 0.5:
        reasons.append("Some key concepts are covered.")
    else:
        reasons.append("Key concepts are missing.")

    return " ".join(reasons)



def classify_answer(percentage):
    if percentage >= 90:
        return "Perfect Answer"
    elif percentage >= 50:
        return "Relevant Answer"
    else:
        return "Irrelevant Answer"