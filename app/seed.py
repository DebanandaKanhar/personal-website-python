from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Category

DEFAULT_CATEGORIES = [
    {
        "name": "AI & ML",
        "slug": "ai-ml",
        "description": "Artificial Intelligence and Machine Learning articles",
        "color": "#8b5cf6",
    },
    {
        "name": "Agents",
        "slug": "agents",
        "description": "AI Agents, AutoGen, LangChain and more",
        "color": "#3b82f6",
    },
    {
        "name": "Use Cases",
        "slug": "use-cases",
        "description": "Real-world AI/ML use cases and applications",
        "color": "#10b981",
    },
    {
        "name": "Teaching",
        "slug": "teaching",
        "description": "Data Science and Computer Science teaching content",
        "color": "#f59e0b",
    },
    {
        "name": "Personal Life",
        "slug": "personal-life",
        "description": "Family, friends and personal experiences",
        "color": "#ec4899",
    },
    {
        "name": "Technology",
        "slug": "technology",
        "description": "General technology articles and opinions",
        "color": "#06b6d4",
    },
]


def run_seed(db: Session):
    for item in DEFAULT_CATEGORIES:
        exists = db.query(Category).filter(Category.slug == item["slug"]).first()
        if exists:
            continue
        db.add(Category(**item))
    db.commit()


if __name__ == "__main__":
    session = SessionLocal()
    try:
        run_seed(session)
        print("Seed completed.")
    finally:
        session.close()
