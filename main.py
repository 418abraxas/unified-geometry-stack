# main.py
from fastapi import FastAPI
from api import (
    router_lex, router_bridge, router_darkzone,
    router_smg, router_mgi, router_telemetry
)
from core.database import Base, engine

app = FastAPI(title="Unified Geometry Stack API", version="vΣ.∞")

# Initialize DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(router_lex.router)
app.include_router(router_bridge.router)
app.include_router(router_darkzone.router)
app.include_router(router_smg.router)
app.include_router(router_mgi.router)
app.include_router(router_telemetry.router)

@app.get("/")
def index():
    return {"message": "Unified Geometry Stack API running."}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/healthz")
def healthz():
    return JSONResponse({"status": "ok"})



