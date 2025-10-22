# api/router_bridge.py
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from core.database import get_db
from models.db_models import BridgeDB

router = APIRouter(prefix="/bridge", tags=["Bridge"])

@router.post("")
def create_bridge(
    relation: dict = Body(..., description="Bridge relation payload"),
    db: Session = Depends(get_db)
):
    """
    Store a new bridge relation in the database.
    """
    record = BridgeDB(payload={
        "relation": relation,
        "timestamp": datetime.utcnow().isoformat()
    })
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"Bridge_ID": str(record.id), "status": "stored", "payload": record.payload}

@router.get("")
def list_bridges(db: Session = Depends(get_db), limit: int = 10):
    """
    Retrieve the most recent bridges.
    """
    rows = db.query(BridgeDB).order_by(BridgeDB.created_at.desc()).limit(limit).all()
    return [{"id": str(r.id), "payload": r.payload} for r in rows]


