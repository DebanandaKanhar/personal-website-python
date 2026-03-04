from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Post
from ..schemas import LoginRequest, PostCreate, PostUpdate
from ..security import create_access_token, get_current_admin, verify_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


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


@router.post("/login")
def login(payload: LoginRequest):
    if not verify_admin(payload.email, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(subject=payload.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/posts")
def admin_posts(
    _: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    posts = (
        db.query(Post).options(joinedload(Post.category)).order_by(Post.created_at.desc())
    ).all()
    return {"posts": [_to_post_dict(p) for p in posts]}


@router.post("/posts")
def create_post(
    payload: PostCreate,
    _: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    exists = db.query(Post).filter(Post.slug == payload.slug).first()
    if exists:
        raise HTTPException(status_code=400, detail="Slug already exists")

    post = Post(
        title=payload.title,
        slug=payload.slug,
        excerpt=payload.excerpt,
        content=payload.content,
        cover_image=payload.cover_image,
        category_id=payload.category_id,
        tags=",".join(payload.tags),
        status=payload.status,
        featured=payload.featured,
        reading_time=payload.reading_time,
    )
    if post.status == "published":
        post.published_at = datetime.utcnow()

    db.add(post)
    db.commit()
    db.refresh(post)
    return {"post": _to_post_dict(post)}


@router.put("/posts/{post_id}")
def update_post(
    post_id: str,
    payload: PostUpdate,
    _: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    updates = payload.model_dump(exclude_none=True)
    if "tags" in updates:
        updates["tags"] = ",".join(updates["tags"])
    if updates.get("status") == "published" and post.published_at is None:
        updates["published_at"] = datetime.utcnow()

    for key, value in updates.items():
        setattr(post, key, value)
    post.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(post)
    return {"post": _to_post_dict(post)}


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: str,
    _: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"success": True}
