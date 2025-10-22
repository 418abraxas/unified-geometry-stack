# api/router_lex.py
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from hashlib import sha256
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from core.database import get_db, engine, Base
from models.db_models import ConceptNodeDB

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/lex", tags=["Lexicon"])

class ConsentVector(BaseModel):
    Psi_sig: str
    phi_sig: str
    dual: bool = True

class Query(BaseModel):
    tok: Optional[str] = None
    span: Optional[str] = None

@router.post("/encode")
def encode(artifact: str = Body(..., embed=True), consent: ConsentVector = Body(...), db: Session = Depends(get_db)):
    bytes_hash = sha256(artifact.encode()).hexdigest()
    payload = {
        "coords": {"x": [0.01] * 32, "theta": 0.2, "r": 0.7, "conf": 0.9},
        "provenance": {"EncoderCardHash": "Φ_enc_vΣ", "timestamp": datetime.utcnow().isoformat()},
        "metrics": {"dH_nearest": 0.0, "Lambda": 0.0, "DeltaK": 0.0},
        "tags": ["ENCODED"],
        "consent": consent.model_dump(),
    }
    node = ConceptNodeDB(artifact=artifact, bytes_hash=bytes_hash, payload=payload)
    db.add(node)
    db.commit()
    db.refresh(node)
    return {"ConceptNode": node.id, "Artifact": artifact, "Anchor_ID": str(node.id)}

@router.post("/retrieve")
def retrieve(query: Query = Body(...), K: int = Body(5, embed=True), db: Session = Depends(get_db)):
    term = query.tok or query.span
    if not term:
        raise HTTPException(status_code=400, detail="Provide tok or span in query")

    candidates = (
        db.query(ConceptNodeDB)
        .filter(ConceptNodeDB.artifact.ilike(f"%{term}%"))
        .order_by(ConceptNodeDB.created_at.desc())
        .limit(K)
        .all()
    )
    results = [
        {
            "node": str(c.id),
            "artifact": c.artifact,
            "d_H": 0.1 * i,
            "S_exp": round(1.0 / (1 + i), 2),
            "tag": "RELATED_NEAR" if i < 3 else "RELATED_FAR",
            "Λ": 0.5 + 0.1 * i,
        }
        for i, c in enumerate(candidates)
    ]
    return {"candidates": results}

@router.post("/conceptify")
def conceptify(text: str = Body(..., embed=True)):
    tokens = text.split()
    nodes = [{"token": t, "concept_id": sha256(t.encode()).hexdigest()[:8]} for t in tokens]
    return {"nodes": nodes}
