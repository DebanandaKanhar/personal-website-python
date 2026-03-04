from pathlib import Path

import joblib

ARTIFACT_DIR = Path("artifacts")


def recommend_for_slug(slug: str, top_k: int = 5) -> list[str]:
    slugs = joblib.load(ARTIFACT_DIR / "slugs.joblib")
    cosine_sim = joblib.load(ARTIFACT_DIR / "cosine_sim.joblib")

    if slug not in slugs:
        return []

    idx = slugs.index(slug)
    similar = list(enumerate(cosine_sim[idx]))
    similar = sorted(similar, key=lambda x: x[1], reverse=True)
    recommended = [slugs[i] for i, _ in similar[1 : top_k + 1]]
    return recommended
