from fastapi import FastAPI
from app.db.base import Base, engine
from app.company.routes import public as company_public, private as company_private
from app.robots.routes import public as robots_public
from app.robots.routes import private as robots_private
from app.auth.routes import router as auth_router

app = FastAPI(title="Robot Suisse API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth_router, tags=["Authentication"])
app.include_router(company_public.router, tags=["Companies"])
app.include_router(company_private.router, tags=["Companies Private"])
app.include_router(robots_public.router, tags=["Robots"])
app.include_router(robots_private.router, tags=["Robots Private"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
