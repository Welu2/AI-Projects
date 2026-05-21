
from fastapi import FastAPI
# 1. Import your modular router
from api.diagnostics import router as diagnostics_router

app = FastAPI(
    title="Enterprise AI Cluster Gateway",
    description="Decoupled micro-service infrastructure registry.",
    version="1.1.0"
)

# 2. Register the isolated router module into the core application engine
app.include_router(diagnostics_router)

@app.get("/")
def read_root():
    return {"message": "Central Infrastructure Gateway Online"}
