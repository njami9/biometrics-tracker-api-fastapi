# app/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .db import create_tables, get_db
from .routers import deliverables, program_qc, qc_comments, personnel, specs
from .routers.toc import tables as toc_tables, figures as toc_figures, listings as toc_listings

app = FastAPI(title="Biometrics Tracker API", version="1.0.0")


# Run table creation on startup
@app.on_event("startup")
def on_startup():
    create_tables()


# Enable CORS (loose for dev; restrict origins for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/v1/healthz")
def healthz():
    return {"ok": True}


# DB ping
@app.get("/v1/db/ping")
def db_ping(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"db": "ok"}


# Routers
app.include_router(deliverables.router, prefix="/v1", tags=["deliverables"])
app.include_router(program_qc.router, prefix="/v1", tags=["program_qc"])
app.include_router(qc_comments.router, prefix="/v1", tags=["qc_comments"])
app.include_router(personnel.router, prefix="/v1", tags=["personnel"])
app.include_router(specs.router, prefix="/v1", tags=["specs"])
app.include_router(toc_tables.router, prefix="/v1", tags=["toc"])
app.include_router(toc_figures.router, prefix="/v1", tags=["toc"])
app.include_router(toc_listings.router, prefix="/v1", tags=["toc"])
