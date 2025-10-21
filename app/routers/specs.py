
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData

from ..db import get_db
from ..models import SpecTable, SpecDataset, Metadata

router = APIRouter()

# GET /v1/specs — returns table_name values from spec_tables
@router.get("/specs", response_model=List[str])
def list_spec_tables(db: Session = Depends(get_db)):
    stmt = select(SpecTable.table_name)
    return [row[0] for row in db.execute(stmt).all()]

# GET /v1/specs/datasets — returns dataset names from spec_datasets
@router.get("/specs/datasets", response_model=List[str])
def list_datasets(db: Session = Depends(get_db)):
    stmt = select(SpecDataset.dataset_name)
    return [row[0] for row in db.execute(stmt).all()]

# GET /v1/specs/datasets/{dataset} — returns rows from the dataset table
@router.get("/specs/datasets/{dataset}")
def get_dataset_rows(dataset: str, db: Session = Depends(get_db)):
    # Validate dataset exists
    allowed = db.execute(select(SpecDataset.dataset_name)).scalars().all()
    if dataset not in allowed:
        raise HTTPException(status_code=404, detail="Dataset not found")

    metadata_obj = MetaData()
    target_table = Table(dataset, metadata_obj, autoload_with=db.bind)

    stmt = select(target_table)
    return [dict(row._mapping) for row in db.execute(stmt).all()]

# GET /v1/specs/datasets/{dataset}/variables — returns rows in metadata filtered to dataset
@router.get("/specs/datasets/{dataset}/variables")
def get_dataset_variables(dataset: str, db: Session = Depends(get_db)):
    stmt = select(Metadata).where(Metadata.dataset_name == dataset)
    return [row._mapping for row in db.execute(stmt).all()]

# GET /v1/specs/{table} — returns rows from a whitelisted table
@router.get("/specs/{table}")
def get_table_rows(
    table: str,
    q: Optional[str] = Query(default=None, description="Search across text columns"),
    db: Session = Depends(get_db),
):
    # Validate table exists in spec_tables
    allowed = db.execute(select(SpecTable.table_name)).scalars().all()
    if table not in allowed:
        raise HTTPException(status_code=404, detail="Table not whitelisted")

    # Reflect table dynamically
    metadata_obj = MetaData()
    target_table = Table(table, metadata_obj, autoload_with=db.bind)

    stmt = select(target_table)
    if q:
        text_cols = [c for c in target_table.columns if "CHAR" in str(c.type).upper() or "TEXT" in str(c.type).upper()]
        like = f"%{q.lower()}%"
        stmt = stmt.where(or_(*[func.lower(c).like(like) for c in text_cols]))

    return [dict(row._mapping) for row in db.execute(stmt).all()]
