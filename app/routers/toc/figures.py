# app/routers/toc/figures.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import Session

from ...db import get_db
from ...models import TOCItem
from ...schemas import TOCItemOut

router = APIRouter()

@router.get("/toc/figures", response_model=List[TOCItemOut])
def list_toc_figures(
    q: Optional[str] = Query(default=None, description="Filter by code or title substring"),
    status_filter: Optional[str] = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(TOCItem).where(TOCItem.type == "figure")
    conds = []
    if q:
        like = f"%{q.lower()}%"
        conds.append(or_(func.lower(TOCItem.code).like(like),
                         func.lower(TOCItem.title).like(like)))
    if status_filter:
        conds.append(TOCItem.status == status_filter)
    if conds:
        stmt = stmt.where(and_(*conds))
    stmt = stmt.order_by(TOCItem.priority.asc().nulls_last(), TOCItem.code.asc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()