from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func

class Base(DeclarativeBase):
    pass

class Deliverable(Base):
    __tablename__ = "deliverables"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
