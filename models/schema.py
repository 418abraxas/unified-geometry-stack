from pydantic import BaseModel
from typing import List, Optional, Any

class ConsentVector(BaseModel):
    Psi_sig: str
    phi_sig: str
    dual: bool = True

class Coordinates(BaseModel):
    x: List[float]
    theta: float
    r: float
    conf: float

class ConceptNode(BaseModel):
    id: str
    coords: Coordinates
    payload: dict
    provenance: dict
    metrics: dict
    tags: List[str] = []

class DarkNode(BaseModel):
    id: str
    coords: Coordinates
    payload: dict
    conf: float
    tag: str
    boundary_hash: str

class GlyphEvent(BaseModel):
    id: str
    glyph: str
    source: str
    t: str
    metrics: dict

class GlyphChain(BaseModel):
    id: str
    events: List[GlyphEvent]
    timespan: List[str]
    stats: dict
    status: str

class Archetype(BaseModel):
    id: str
    name: str
    sigil: Optional[str] = None
    roles: List[str] = []
    priors: dict = {}
    themes: List[str] = []
    provenance: Optional[str] = None

class MythThread(BaseModel):
    id: str
    title: str
    events: List[str]
    metrics: dict
    status: str

class EpochMap(BaseModel):
    id: str
    epoch_range: str
    archetype_layers: dict
    hotspots: List[str]
    voids: List[str]
    hash: str
