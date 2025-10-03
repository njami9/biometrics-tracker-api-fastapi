# app/routers/qc_comments.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import QCComment
from ..schemas import QCCommentCreate, QCCommentUpdate, QCCommentOut

router = APIRouter()

@router.get("/qc_comments", response_model=List[QCCommentOut])
def list_qc_comments(
    program_qc_id: Optional[int] = Query(default=None),
    resolved: Optional[bool] = Query(default=None),
    q: Optional[str] = Query(default=None, description="Filter by author or comment_text"),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(QCComment)
    conds = []
    if program_qc_id is not None:
        conds.append(QCComment.program_qc_id == program_qc_id)
    if resolved is not None:
        conds.append(QCComment.resolved == resolved)
    if q:
        like = f"%{q.lower()}%"
        conds.append(
            or_(
                func.lower(QCComment.author).like(like),
                func.lower(QCComment.comment_text).like(like),
            )
        )
    if conds:
        stmt = stmt.where(and_(*conds))
    stmt = stmt.order_by(QCComment.created_at.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()

@router.get("/qc_comments/{comment_id}", response_model=QCCommentOut)
def get_qc_comment(comment_id: int, db: Session = Depends(get_db)):
    obj = db.get(QCComment, comment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="QCComment not found")
    return obj

@router.post("/qc_comments", response_model=QCCommentOut, status_code=status.HTTP_201_CREATED)
def create_qc_comment(payload: QCCommentCreate, db: Session = Depends(get_db)):
    obj = QCComment(
        program_qc_id=payload.program_qc_id,
        author=payload.author,
        comment_text=payload.comment_text,
        resolved=bool(payload.resolved) if payload.resolved is not None else False,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.patch("/qc_comments/{comment_id}", response_model=QCCommentOut)
def update_qc_comment(comment_id: int, payload: QCCommentUpdate, db: Session = Depends(get_db)):
    obj = db.get(QCComment, comment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="QCComment not found")

    if payload.author is not None:
        obj.author = payload.author
    if payload.comment_text is not None:
        obj.comment_text = payload.comment_text
    if payload.resolved is not None:
        obj.resolved = payload.resolved

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/qc_comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_qc_comment(comment_id: int, db: Session = Depends(get_db)):
    obj = db.get(QCComment, comment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="QCComment not found")
    db.delete(obj)
    db.commit()
    return