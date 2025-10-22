# api/router_lex.py
from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Optional
from hashlib import sha256
from datetime import datetime
import uuid, os, json
from core.vault import write_vault

router = APIRouter(prefix="/lex", tags=["Lexicon"])

class ConsentVector(BaseModel):
    Psi_sig: str
    phi_sig: str
    dual: bool = True

class Query(BaseModel):
    tok: Optional[str] = None
    span: Optional[str] = None

# ----- /lex/encode -----
@router.post("/encode")
def encode(artifact: str = Body(..., embed=True), consent: ConsentVector = Body(...)):
    coords = {"x": [0.01] * 32, "theta": 0.2, "r": 0.7, "conf": 0.9}
    anchor_id = sha256(f"{artifact}{datetime.utcnow()}".encode()).hexdigest()
    node = {
        "id": str(uuid.uuid4()),
        "coords": coords,
        "payload": {
            "kind": "text",
            "bytes_hash": sha256(artifact.encode()).hexdigest()
        },
        "provenance": {
            "EncoderCardHash": "Φ_enc_vΣ",
            "timestamp": datetime.utcnow().isoformat()
        },
        "metrics": {"dH_nearest": 0.0, "Lambda": 0.0, "DeltaK": 0.0},
        "tags": ["ENCODED"]
    }
    write_vault("Concepts", node, anchor_id)
    return {"ConceptNode": node, "Anchor_ID": anchor_id}

# ----- /lex/retrieve -----
@router.post("/retrieve")
def retrieve(query: Query = Body(...), K: int = Body(5, embed=True)):
    term = query.tok or query.span or ""
    # For now return dummy candidates
    candidates = [
        {
            "node": term + f"_{i}",
            "d_H": round(0.1 * i, 2),
            "S_exp": round(1.0 / (1 + i), 2),
            "tag": "RELATED_NEAR" if i < 3 else "RELATED_FAR",
            "Λ": 0.5 + 0.1 * i
        }
        for i in range(K)
    ]
    return {"candidates": candidates}

# ----- /lex/conceptify -----
@router.post("/conceptify")
def conceptify(text: str = Body(..., embed=True)):
    # simple mock
    tokens = text.split()
    nodes = [{"token": t, "concept_id": sha256(t.encode()).hexdigest()[:8]} for t in tokens]
    return {"nodes": nodes}
