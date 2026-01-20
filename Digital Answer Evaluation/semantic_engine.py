import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import SBERT_MODEL_NAME

nltk.download("punkt")

model = SentenceTransformer(SBERT_MODEL_NAME)

def sentence_level_similarity(student_text: str, reference_text: str) -> float:
    """
    Computes sentence-level cosine similarity using SBERT.
    Returns the best matching sentence similarity.
    """
    student_sentences = nltk.sent_tokenize(student_text)
    ref_embedding = model.encode(reference_text)

    scores = []

    for sent in student_sentences:
        sent_embedding = model.encode(sent)
        score = cosine_similarity(
            [sent_embedding],
            [ref_embedding]
        )[0][0]
        scores.append(score)

    return max(scores) if scores else 0.0