from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.get("/{stream}")
def telemetry(stream: str):
    return {"stream": stream, "status": "ok", "timestamp": datetime.utcnow().isoformat()}
