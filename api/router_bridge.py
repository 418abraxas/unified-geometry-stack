from fastapi import APIRouter
from models.schema import Coordinates

router = APIRouter(prefix="/bridge", tags=["Relations"])

@router.post("")
def bridge(Xa: Coordinates, Xb: Coordinates, cap: float = 0.8, k_max: int = 4):
    return {
        "segments": [{"from": 0, "to": 1, "d_H": 0.7, "tag": "RELATED_NEAR"}],
        "Z": [Xa, Xb],
        "meta": {"mean_dH": 0.7, "max_dH": 0.7}
    }
