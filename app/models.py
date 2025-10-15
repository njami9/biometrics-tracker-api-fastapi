'''
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func

class Base(DeclarativeBase):
    pass

class Deliverable(Base):
    _tablename__ = "deliverables"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
'''
# app/models.py

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Date, ForeignKey
from .db import Base


# ---- Deliverables ----
class Deliverable(Base):
    __tablename__ = "deliverables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)


# ---- Program QC ----
class ProgramQC(Base):
    __tablename__ = "program_qc"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    program_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    assignee: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    reviewer: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    deliverable_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("deliverables.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


# ---- QC Comments ----
class QCComment(Base):
    __tablename__ = "qc_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    program_qc_id: Mapped[int] = mapped_column(
        ForeignKey("program_qc.id"), nullable=False
    )
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    resolved: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    

class Personnel(Base):
    __tablename__ = "personnel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    preferred_name: Mapped[Optional[str]] = mapped_column(String, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String, index=True)
    status: Mapped[Optional[str]] = mapped_column(String, index=True)


# ---- TOC Items (shared model for tables/figures/listings) ----
class TOCItem(Base):
    __tablename__ = "toc_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(10), nullable=False)  # 'table' | 'figure' | 'listing'
    code: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., t_14_1_01
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    dataset: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    priority: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
