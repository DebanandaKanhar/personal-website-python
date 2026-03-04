from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, desc, or_
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Category, Post

router = APIRouter(prefix="/api", tags=["public"])


def _to_post_dict(post: Post) -> dict:
    tags = post.tags.split(",") if post.tags else []
    return {
        "id": post.id,
        "title": post.title,
        "slug": post.slug,
        "excerpt": post.excerpt,
        "content": post.content,
        "cover_image": post.cover_image,
        "category_id": post.category_id,
        "tags": tags,
        "status": post.status,
        "featured": post.featured,
        "reading_time": post.reading_time,
        "view_count": post.view_count,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "published_at": post.published_at,
        "category": post.category,
    }


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.name.asc()).all()
    return {"categories": categories}


@router.get("/posts")
def get_posts(
    cat: str | None = Query(default=None),
    q: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Post).options(joinedload(Post.category))

    if status:
        query = query.filter(Post.status == status)
    else:
        query = query.filter(Post.status == "published")

    if cat:
        query = query.join(Category, Post.category_id == Category.id).filter(
            Category.slug == cat
        )

    if q:
        like_query = f"%{q}%"
        query = query.filter(
            or_(Post.title.ilike(like_query), Post.excerpt.ilike(like_query))
        )

    posts = query.order_by(desc(Post.published_at), desc(Post.created_at)).all()
    return {"posts": [_to_post_dict(p) for p in posts]}


@router.get("/posts/{slug}")
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    post = (
        db.query(Post)
        .options(joinedload(Post.category))
        .filter(and_(Post.slug == slug, Post.status == "published"))
        .first()
    )
    if not post:
        return {"post": None}
    return {"post": _to_post_dict(post)}
