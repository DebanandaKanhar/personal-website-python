from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
    description: Optional[str] = None
    color: str


class PostBase(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str = ""
    cover_image: Optional[str] = None
    category_id: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    status: str = "draft"
    featured: bool = False
    reading_time: int = 5


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[list[str]] = None
    status: Optional[str] = None
    featured: Optional[bool] = None
    reading_time: Optional[int] = None


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    cover_image: Optional[str] = None
    category_id: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    status: str
    featured: bool
    reading_time: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    category: Optional[CategoryOut] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PageViewIn(BaseModel):
    path: str
    referrer: Optional[str] = None
    user_agent: str = ""


class DailyViewPoint(BaseModel):
    date: str
    views: int
