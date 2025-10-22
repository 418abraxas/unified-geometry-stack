from fastapi import APIRouter, Body
from hashlib import sha256
from datetime import datetime
import uuid
from models.schema import ConsentVector, ConceptNode, Coordinates
from core.vault import write_vault

router = APIRouter(prefix="", tags=["Core"])

@router.post("/encode")
def encode(artifact: str = Body(..., embed=True), consent: ConsentVector = Body(...)):
    x = [0.01] * 32
    coords = Coordinates(x=x, theta=0.2, r=0.7, conf=0.9)
    anchor_id = sha256(f"{artifact}{datetime.utcnow()}".encode()).hexdigest()
    node = ConceptNode(
        id=str(uuid.uuid4()),
        coords=coords,
        payload={"kind": "text", "bytes_hash": sha256(artifact.encode()).hexdigest()},
        provenance={"EncoderCardHash": "Φ_enc_vΣ", "timestamp": datetime.utcnow().isoformat()},
        metrics={"dH_nearest": 0.0, "Lambda": 0.0, "DeltaK": 0.0},
        tags=["ENCODED"]
    )
    write_vault("Concepts", node.dict(), anchor_id)
    return {"ConceptNode": node, "Anchor_ID": anchor_id}
