from fastapi import APIRouter
from models.schema import GlyphEvent, GlyphChain
import uuid, datetime

router = APIRouter(prefix="/smg", tags=["SemanticMemory"])

@router.post("/ingest")
def ingest(seq: str):
    ev = GlyphEvent(
        id=str(uuid.uuid4()), glyph=seq[:4], source="ingest", t=str(datetime.datetime.utcnow()),
        metrics={"d_H": 0.1, "Λ": 0.5, "Δκ": 0.02, "conf": 0.9}
    )
    chain = GlyphChain(
        id=str(uuid.uuid4()),
        events=[ev],
        timespan=[ev.t],
        stats={"mean_dH": 0.1},
        status="ACTIVE"
    )
    return chain
