from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, desc, or_
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Category, Post

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    featured = (
        db.query(Post)
        .options(joinedload(Post.category))
        .filter(and_(Post.status == "published", Post.featured.is_(True)))
        .order_by(desc(Post.published_at), desc(Post.created_at))
        .limit(6)
        .all()
    )
    latest = (
        db.query(Post)
        .options(joinedload(Post.category))
        .filter(Post.status == "published")
        .order_by(desc(Post.published_at), desc(Post.created_at))
        .limit(10)
        .all()
    )
    categories = db.query(Category).order_by(Category.name.asc()).all()
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "featured_posts": featured,
            "latest_posts": latest,
            "categories": categories,
        },
    )


@router.get("/articles")
def articles(
    request: Request,
    cat: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(Post)
        .options(joinedload(Post.category))
        .filter(Post.status == "published")
    )

    if cat:
        query = query.join(Category, Post.category_id == Category.id).filter(
            Category.slug == cat
        )

    if q:
        like_q = f"%{q}%"
        query = query.filter(
            or_(Post.title.ilike(like_q), Post.excerpt.ilike(like_q), Post.content.ilike(like_q))
        )

    posts = query.order_by(desc(Post.published_at), desc(Post.created_at)).all()
    categories = db.query(Category).order_by(Category.name.asc()).all()
    return templates.TemplateResponse(
        "articles.html",
        {
            "request": request,
            "posts": posts,
            "categories": categories,
            "active_category": cat,
            "search_query": q or "",
        },
    )


@router.get("/articles/{slug}")
def article_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    post = (
        db.query(Post)
        .options(joinedload(Post.category))
        .filter(and_(Post.slug == slug, Post.status == "published"))
        .first()
    )
    related = []
    if post and post.category_id:
        related = (
            db.query(Post)
            .filter(
                and_(
                    Post.status == "published",
                    Post.category_id == post.category_id,
                    Post.slug != slug,
                )
            )
            .order_by(desc(Post.published_at), desc(Post.created_at))
            .limit(5)
            .all()
        )
    return templates.TemplateResponse(
        "article_detail.html",
        {"request": request, "post": post, "related_posts": related},
    )


@router.get("/admin")
def admin_portal(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
