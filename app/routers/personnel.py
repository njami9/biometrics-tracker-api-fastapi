# app/routers/personnel.py
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Personnel
from ..schemas import PersonnelCreate, PersonnelUpdate, PersonnelOut

router = APIRouter()


@router.get("/personnel", response_model=List[PersonnelOut])
def list_personnel(
    q: Optional[str] = Query(
        default=None,
        description="Case-insensitive search across preferred_name and full_name"
    ),
    status_filter: Optional[str] = Query(default=None, alias="status"),
    member_id: Optional[int] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):

    stmt = select(Personnel)
    conds = []

    if q:
        like = f"%{q.lower()}%"
        conds.append(
            or_(
                func.lower(Personnel.preferred_name).like(like),
                func.lower(Personnel.full_name).like(like),
            )
        )

    if status_filter:
        conds.append(Personnel.status == status_filter)

    if member_id is not None:
        conds.append(Personnel.member_id == member_id)

    if conds:
        stmt = stmt.where(and_(*conds))

    # Order by name (case-insensitive). Avoid NULLS LAST for cross-DB portability.
    stmt = stmt.order_by(
        func.lower(Personnel.full_name).asc(),
        func.lower(Personnel.preferred_name).asc(),
        Personnel.id.asc(),
    ).limit(limit).offset(offset)

    return db.execute(stmt).scalars().all()


@router.get("/personnel/{id}", response_model=PersonnelOut)
def get_personnel(id: int, db: Session = Depends(get_db)):

    obj = db.get(Personnel, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Personnel record not found")
    return obj


@router.post("/personnel", response_model=PersonnelOut, status_code=status.HTTP_201_CREATED)
def create_personnel(payload: PersonnelCreate, db: Session = Depends(get_db)):
    values = payload.model_dump(exclude_unset=True)
    obj = Personnel(**values)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/personnel/{id}", response_model=PersonnelOut)
def update_personnel(id: int, payload: PersonnelUpdate, db: Session = Depends(get_db)):
    obj = db.get(Personnel, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Personnel record not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(obj, field, value)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/personnel/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_personnel(id: int, db: Session = Depends(get_db)):
    obj = db.get(Personnel, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Personnel record not found")

    db.delete(obj)
    db.commit()
    return
