import hashlib
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import PageView, Post, Visitor
from ..schemas import PageViewIn

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def get_device_type(user_agent: str) -> str:
    ua = user_agent.lower()
    if "mobile" in ua:
        return "mobile"
    if "tablet" in ua or "ipad" in ua:
        return "tablet"
    return "desktop"


def get_browser(user_agent: str) -> str:
    ua = user_agent.lower()
    if "chrome" in ua and "edg" not in ua:
        return "Chrome"
    if "firefox" in ua:
        return "Firefox"
    if "safari" in ua and "chrome" not in ua:
        return "Safari"
    if "edg" in ua:
        return "Edge"
    return "Other"


@router.post("/pageview")
def track_pageview(payload: PageViewIn, request: Request, db: Session = Depends(get_db)):
    client_ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    if not client_ip:
        client_ip = request.client.host if request.client else "0.0.0.0"

    visitor_hash = hashlib.sha256(
        f"{client_ip}{settings.app_secret_key}".encode("utf-8")
    ).hexdigest()[:16]

    page_view = PageView(
        page_path=payload.path,
        visitor_hash=visitor_hash,
        device_type=get_device_type(payload.user_agent),
        browser=get_browser(payload.user_agent),
        referrer=payload.referrer,
    )
    db.add(page_view)

    visitor = db.query(Visitor).filter(Visitor.visitor_hash == visitor_hash).first()
    if visitor:
        visitor.last_visit = datetime.utcnow()
        visitor.visit_count += 1
    else:
        db.add(Visitor(visitor_hash=visitor_hash, visit_count=1))

    if payload.path.startswith("/articles/"):
        slug = payload.path.removeprefix("/articles/").strip("/")
        post = db.query(Post).filter(Post.slug == slug).first()
        if post:
            post.view_count += 1

    db.commit()
    return {"ok": True}


@router.get("/stats")
def stats(
    type: str = Query(default="overview"),
    days: int = Query(default=30),
    db: Session = Depends(get_db),
):
    if type == "total-visitors":
        total = db.query(Visitor).count()
        return {"total": total}

    if type == "overview":
        now = datetime.utcnow()
        today = datetime(now.year, now.month, now.day)
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        return {
            "totalVisitors": db.query(Visitor).count(),
            "todayViews": db.query(PageView)
            .filter(PageView.created_at >= today)
            .count(),
            "weekViews": db.query(PageView)
            .filter(PageView.created_at >= week_ago)
            .count(),
            "monthViews": db.query(PageView)
            .filter(PageView.created_at >= month_ago)
            .count(),
            "totalPosts": db.query(Post).count(),
        }

    if type == "daily-views":
        start = datetime.utcnow() - timedelta(days=days)
        rows = (
            db.query(func.date(PageView.created_at), func.count(PageView.id))
            .filter(PageView.created_at >= start)
            .group_by(func.date(PageView.created_at))
            .all()
        )
        return {"data": [{"date": str(date), "views": count} for date, count in rows]}

    if type == "top-pages":
        rows = (
            db.query(PageView.page_path, func.count(PageView.id).label("views"))
            .group_by(PageView.page_path)
            .order_by(func.count(PageView.id).desc())
            .limit(10)
            .all()
        )
        return {"data": [{"page": page, "views": views} for page, views in rows]}

    if type == "devices":
        rows = (
            db.query(PageView.device_type, func.count(PageView.id))
            .group_by(PageView.device_type)
            .all()
        )
        return {
            "data": [
                {"name": name or "unknown", "value": value} for name, value in rows
            ]
        }

    if type == "browsers":
        rows = (
            db.query(PageView.browser, func.count(PageView.id))
            .group_by(PageView.browser)
            .all()
        )
        return {
            "data": [{"name": name or "Other", "value": value} for name, value in rows]
        }

    return {"error": "Invalid type"}
