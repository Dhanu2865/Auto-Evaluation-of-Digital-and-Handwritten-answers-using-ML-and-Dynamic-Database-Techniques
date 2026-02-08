from database import SessionLocal
from models import EvaluationResult

def clear_pending_reviews():
    db = SessionLocal()

    deleted = db.query(EvaluationResult).filter(
        EvaluationResult.status == "PENDING"
    ).delete()

    db.commit()
    db.close()

    print(f"✅ Cleared {deleted} pending review(s).")

if __name__ == "__main__":
    clear_pending_reviews()
