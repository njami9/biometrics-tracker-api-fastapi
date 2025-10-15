from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeliverableCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    status: Optional[str] = Field(default=None, max_length=50)

class DeliverableOut(BaseModel):
    id: int
    name: str
    status: Optional[str] = None
    class Config:
        from_attributes = True


# --- Program QC ---
class ProgramQCBase(BaseModel):
    program_name: str
    status: Optional[str] = None
    assignee: Optional[str] = None
    reviewer: Optional[str] = None
    deliverable_id: Optional[int] = None

class ProgramQCCreate(ProgramQCBase):
    pass

class ProgramQCUpdate(BaseModel):
    program_name: Optional[str] = None
    status: Optional[str] = None
    assignee: Optional[str] = None
    reviewer: Optional[str] = None
    deliverable_id: Optional[int] = None

class ProgramQCOut(BaseModel):
    id: int
    program_name: str
    status: Optional[str] = None
    assignee: Optional[str] = None
    reviewer: Optional[str] = None
    deliverable_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pydantic v2: serialize SQLAlchemy models

# --- QC Comments ---
class QCCommentBase(BaseModel):
    program_qc_id: int
    author: str
    comment_text: str
    resolved: Optional[bool] = False

class QCCommentCreate(QCCommentBase):
    pass

class QCCommentUpdate(BaseModel):
    author: Optional[str] = None
    comment_text: Optional[str] = None
    resolved: Optional[bool] = None

class QCCommentOut(BaseModel):
    id: int
    program_qc_id: int
    author: str
    comment_text: str
    resolved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Personnel ---
class PersonnelBase(BaseModel):
    member_id: Optional[int] = None
    preferred_name: Optional[str] = None
    full_name: Optional[str] = None
    status: Optional[str] = None

class PersonnelCreate(PersonnelBase):
    pass

class PersonnelUpdate(BaseModel):
    member_id: Optional[int] = None
    preferred_name: Optional[str] = None
    full_name: Optional[str] = None
    status: Optional[str] = None

class PersonnelOut(PersonnelBase):
    id: int
    member_id: Optional[int] = None
    preferred_name: Optional[str] = None
    full_name: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = True  


# --- TOC (read-only list output) ---
class TOCItemOut(BaseModel):
    id: int
    code: str
    title: Optional[str] = None
    status: Optional[str] = None
    dataset: Optional[str] = None
    priority: Optional[int] = None

    class Config:
        from_attributes = True
