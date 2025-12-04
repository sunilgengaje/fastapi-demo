# app/controllers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas
from .database import SessionLocal
from .service import ItemService
import traceback, sys

router = APIRouter(prefix="/items", tags=["items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    service = ItemService(db)
    try:
        created = service.create_item(item)
        # Convert SQLAlchemy object -> Pydantic model (Pydantic v2 style)
        return schemas.ItemRead.model_validate(created)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")
    
@router.get("/{item_id}", response_model=schemas.ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a single item by id.
    """
    service = ItemService(db)
    try:
        db_item = service.get_item(item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        return schemas.ItemRead.model_validate(db_item)
    except HTTPException:
        raise
    except Exception:
        traceback.print_exc(file=sys.stderr)
        raise HTTPException(status_code=500, detail="Internal Server Error")
