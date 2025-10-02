from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routers import health, dbcheck, deliverables
from .db import engine, DB_URL
from .models import Base

app = FastAPI(
    title="Biometrics Tracker API",
    version="0.1.0",
    description="API facade for the SQL-based Biometrics Tracker."
)

# Routers
app.include_router(health.router, prefix="/v1", tags=["health"])
app.include_router(dbcheck.router, prefix="/v1", tags=["diagnostics"])
app.include_router(deliverables.router, prefix="/v1", tags=["deliverables"])

# Auto-create tables for SQLite only
if DB_URL.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
