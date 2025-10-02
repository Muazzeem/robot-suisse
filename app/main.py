from fastapi import FastAPI
from app.db.base import Base, engine

# Import routers
from app.company.routes import public, private

app = FastAPI(title="FastAPI + Postgres CRUD")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(public.router)
app.include_router(private.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
