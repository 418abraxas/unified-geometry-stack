# api/router_telemetry.py
from fastapi import APIRouter, Path, Body, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from core.database import get_db
from models.db_models import TelemetryDB

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.post("/{stream}")
def append_telemetry(
    stream: str = Path(..., description="Stream name"),
    payload: dict = Body(...),
    db: Session = Depends(get_db)
):
    """
    Append a telemetry event to a stream.
    """
    record = TelemetryDB(stream=stream, payload=payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"Telemetry_ID": str(record.id), "stream": stream, "status": "logged"}

@router.get("/{stream}")
def get_stream(
    stream: str = Path(...),
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Retrieve recent telemetry events for a stream.
    """
    rows = (
        db.query(TelemetryDB)
        .filter(TelemetryDB.stream == stream)
        .order_by(TelemetryDB.created_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "stream": stream,
        "records": [{"id": str(r.id), "payload": r.payload} for r in rows]
    }
