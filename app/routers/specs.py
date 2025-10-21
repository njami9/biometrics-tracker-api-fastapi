from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import SpecTable, SpecDataset
from app.schemas import SpecTableOut, SpecDatasetOut
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/specs", response_model=List[str], tags=["specs"])
def get_spec_tables(db: Session = Depends(get_db)):
    tables = db.query(SpecTable).all()
    return [table.table_name for table in tables]

@router.get("/specs/{table}", tags=["specs"])
def get_spec_table_rows(table: str):
    import pandas as pd
    import os

    db_path = f"data/specs/Analysis_Datasets/{table}.csv"
    cross_path = f"data/specs/{table}.csv"

    if os.path.exists(db_path):
        df = pd.read_csv(db_path)
    elif os.path.exists(cross_path):
        df = pd.read_csv(cross_path)
    else:
        raise HTTPException(status_code=404, detail="Table not found")

    return df.to_dict(orient="records")

@router.get("/specs/datasets", response_model=List[str], tags=["specs"])
def get_spec_datasets(db: Session = Depends(get_db)):
    datasets = db.query(SpecDataset).all()
    return [ds.dataset_name for ds in datasets]

@router.get("/specs/datasets/{dataset}", tags=["specs"])
def get_dataset_rows(dataset: str):
    import pandas as pd
    path = f"data/specs/Analysis_Datasets/{dataset}.csv"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Dataset not found")
    df = pd.read_csv(path)
    return df.to_dict(orient="records")

@router.get("/specs/datasets/{dataset}/variables", tags=["specs"])
def get_dataset_variables(dataset: str):
    import pandas as pd
    path = "data/specs/metadata.csv"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Metadata not found")
    df = pd.read_csv(path)
    filtered = df[df["dataset"] == dataset]
    return filtered.to_dict(orient="records")