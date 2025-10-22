from pathlib import Path

VAULT_DIR = Path("Σ_Vault")
VAULT_DIR.mkdir(exist_ok=True)

def vault_path(subdir: str) -> Path:
    p = VAULT_DIR / subdir
    p.mkdir(exist_ok=True)
    return p
