from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello from Railway"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/healthz")
def healthz():
    return JSONResponse({"status": "ok"})
