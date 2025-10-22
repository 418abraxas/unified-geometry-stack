import json, hashlib
from datetime import datetime
from pathlib import Path
from .config import vault_path

def write_vault(subdir: str, payload: dict, anchor_id: str) -> Path:
    path = vault_path(subdir) / f"{anchor_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    append_hash_log(payload, anchor_id)
    return path

def append_hash_log(payload: dict, anchor_id: str):
    log = vault_path("") / "Hashes.log"
    h = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    with open(log, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} sha256={h} Anchor_ID={anchor_id}\n")
