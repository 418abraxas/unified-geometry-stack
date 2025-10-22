# api/router_darkzone.py
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from core.database import get_db
from models.db_models import DarkzoneDB

router = APIRouter(prefix="/darkzone", tags=["DarkZone"])

@router.post("/synthesize")
def synthesize_darkzone(
    boundary_nodes: list = Body(...),
    region: str = Body("unspecified"),
    db: Session = Depends(get_db)
):
    """
    Create a darkzone synthesis record.
    """
    payload = {
        "boundary_nodes": boundary_nodes,
        "region": region,
        "result": {"DarkNode": f"dz_{len(boundary_nodes)}", "confidence": 0.9},
        "timestamp": datetime.utcnow().isoformat()
    }
    record = DarkzoneDB(payload=payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"Darkzone_ID": str(record.id), "payload": record.payload}

@router.get("")
def list_darkzones(db: Session = Depends(get_db), limit: int = 10):
    rows = db.query(DarkzoneDB).order_by(DarkzoneDB.created_at.desc()).limit(limit).all()
    return [{"id": str(r.id), "payload": r.payload} for r in rows]
