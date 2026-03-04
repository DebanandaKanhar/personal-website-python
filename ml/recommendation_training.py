"""
Simple content-based recommendation training job.
Run this in CI or scheduled job to refresh model artifacts.
"""

from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy import create_engine, text

from app.config import settings

ARTIFACT_DIR = Path("artifacts")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def run():
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT slug, title, COALESCE(content, '') AS content
                FROM posts
                WHERE status = 'published'
                """
            )
        ).mappings().all()

    if not rows:
        print("No published posts found. Skipping training.")
        return

    slugs = [row["slug"] for row in rows]
    corpus = [f"{row['title']} {row['content']}" for row in rows]

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    matrix = vectorizer.fit_transform(corpus)
    cosine_sim = linear_kernel(matrix, matrix)

    joblib.dump(vectorizer, ARTIFACT_DIR / "vectorizer.joblib")
    joblib.dump(cosine_sim, ARTIFACT_DIR / "cosine_sim.joblib")
    joblib.dump(slugs, ARTIFACT_DIR / "slugs.joblib")
    print("Artifacts saved to artifacts/ directory.")


if __name__ == "__main__":
    run()
