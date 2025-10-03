# app/routers/program_qc.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ProgramQC
from ..schemas import ProgramQCCreate, ProgramQCUpdate, ProgramQCOut

router = APIRouter()

@router.get("/program_qc", response_model=List[ProgramQCOut])
def list_program_qc(
    q: Optional[str] = Query(default=None, description="Filter by program_name substring"),
    status_filter: Optional[str] = Query(default=None, alias="status"),
    assignee: Optional[str] = None,
    reviewer: Optional[str] = None,
    deliverable_id: Optional[int] = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(ProgramQC)
    conds = []
    if q:
        conds.append(func.lower(ProgramQC.program_name).like(f"%{q.lower()}%"))
    if status_filter:
        conds.append(ProgramQC.status == status_filter)
    if assignee:
        conds.append(ProgramQC.assignee == assignee)
    if reviewer:
        conds.append(ProgramQC.reviewer == reviewer)
    if deliverable_id is not None:
        conds.append(ProgramQC.deliverable_id == deliverable_id)
    if conds:
        stmt = stmt.where(and_(*conds))
    stmt = stmt.order_by(ProgramQC.created_at.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()

@router.get("/program_qc/{qc_id}", response_model=ProgramQCOut)
def get_program_qc(qc_id: int, db: Session = Depends(get_db)):
    obj = db.get(ProgramQC, qc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="ProgramQC not found")
    return obj

@router.post("/program_qc", response_model=ProgramQCOut, status_code=status.HTTP_201_CREATED)
def create_program_qc(payload: ProgramQCCreate, db: Session = Depends(get_db)):
    obj = ProgramQC(
        program_name=payload.program_name,
        status=payload.status,
        assignee=payload.assignee,
        reviewer=payload.reviewer,
        deliverable_id=payload.deliverable_id,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.patch("/program_qc/{qc_id}", response_model=ProgramQCOut)
def update_program_qc(qc_id: int, payload: ProgramQCUpdate, db: Session = Depends(get_db)):
    obj = db.get(ProgramQC, qc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="ProgramQC not found")

    if payload.program_name is not None:
        obj.program_name = payload.program_name
    if payload.status is not None:
        obj.status = payload.status
    if payload.assignee is not None:
        obj.assignee = payload.assignee
    if payload.reviewer is not None:
        obj.reviewer = payload.reviewer
    if payload.deliverable_id is not None:
        obj.deliverable_id = payload.deliverable_id

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/program_qc/{qc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program_qc(qc_id: int, db: Session = Depends(get_db)):
    obj = db.get(ProgramQC, qc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="ProgramQC not found")
    db.delete(obj)
    db.commit()
    return