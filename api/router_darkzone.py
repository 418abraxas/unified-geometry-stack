from fastapi import APIRouter
from hashlib import sha256
import uuid, json
from models.schema import Coordinates, DarkNode
from core.vault import write_vault

router = APIRouter(prefix="/darkzone", tags=["Synthesis"])

@router.post("/synthesize")
def synthesize(boundary_nodes: list[Coordinates]):
    coords = Coordinates(x=[0.02]*32, theta=0.3, r=0.8, conf=0.6)
    dark = DarkNode(
        id=str(uuid.uuid4()),
        coords=coords,
        payload={"summary": "Synthesized node", "tokens": []},
        conf=0.6,
        tag="PROVISIONAL",
        boundary_hash=sha256(json.dumps([n.dict() for n in boundary_nodes]).encode()).hexdigest()
    )
    write_vault("Dark", dark.dict(), dark.id)
    return dark
