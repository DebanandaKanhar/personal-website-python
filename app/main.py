from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from .config import settings
from .database import Base, SessionLocal, engine
from .routers import admin, analytics, public, web
from .seed import run_seed

app = FastAPI(title=settings.app_name, version="1.0.0")


@app.get("/healthz")
def healthcheck():
    return {"status": "ok", "env": settings.app_env}


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    # Seed initial categories once for a ready-to-use CMS.
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()


app.include_router(public.router)
app.include_router(admin.router)
app.include_router(analytics.router)
app.include_router(web.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

Instrumentator().instrument(app).expose(app, include_in_schema=False)
