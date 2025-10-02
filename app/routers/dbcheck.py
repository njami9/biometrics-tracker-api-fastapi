from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..db import get_db

router = APIRouter()

@router.get("/db/ping")
def db_ping(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {"ok": True, "result": result}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {ex}")
