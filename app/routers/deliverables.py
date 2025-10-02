from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from ..models import Deliverable
from ..schemas import DeliverableCreate, DeliverableOut

router = APIRouter()

@router.get("/deliverables", response_model=List[DeliverableOut])
def list_deliverables(
    q: Optional[str] = Query(None, description="Search by name or status (case-insensitive)"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(Deliverable).order_by(Deliverable.id)
    if q:
        like = f"%{q}%"
        stmt = select(Deliverable).where(
            (Deliverable.name.ilike(like)) | (Deliverable.status.ilike(like))
        ).order_by(Deliverable.id)
    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    return rows

@router.get("/deliverables/{deliverable_id}", response_model=DeliverableOut)
def get_deliverable(deliverable_id: int, db: Session = Depends(get_db)):
    row = db.get(Deliverable, deliverable_id)
    if not row:
        raise HTTPException(status_code=404, detail="Deliverable not found")
    return row

@router.post("/deliverables", response_model=DeliverableOut, status_code=201)
def create_deliverable(payload: DeliverableCreate, db: Session = Depends(get_db)):
    rec = Deliverable(name=payload.name, status=payload.status)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
