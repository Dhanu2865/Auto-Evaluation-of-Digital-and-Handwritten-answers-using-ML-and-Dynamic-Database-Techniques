from config import ML_WEIGHT, RULE_WEIGHT

def calculate_final_percentage(ml_score, rule_score):
    final_score = (ML_WEIGHT * ml_score) + (RULE_WEIGHT * rule_score)
    percentage = round(final_score * 100, 2)
    return final_score, percentage