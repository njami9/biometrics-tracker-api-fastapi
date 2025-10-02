from pydantic import BaseModel, Field
from typing import Optional

class DeliverableCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    status: Optional[str] = Field(default=None, max_length=50)

class DeliverableOut(BaseModel):
    id: int
    name: str
    status: Optional[str] = None
    class Config:
        from_attributes = True
