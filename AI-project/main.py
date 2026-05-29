import uuid
import logging
import json
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI(title="AI Infrastructure Resiliency Guard")
logger = logging.getLogger("Telemetry_Logger")

# ------------------------------------------------------------------
# GLOBAL EXCEPTION INTERCEPTORS
# ------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_unhandled_exception_handler(request: Request, exc: Exception):
    """Intercepts every raw unhandled server error across the stack."""
    # Attempt to grab our request correlation ID, fallback to new UUID if missing
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    # 1. Log the exact error structurally for internal infrastructure debugging
    error_payload = {
        "event": "CRITICAL_SYSTEM_ERROR",
        "request_id": request_id,
        "error_type": exc.__class__.__name__,
        "error_detail": str(exc),
        "path": request.url.path
    }
    logger.error(json.dumps(error_payload))
    
    # 2. Return a clean, standardized, secure client response without internal leaks
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error_code": "INTERNAL_INFRASTRUCTURE_FAILURE",
            "message": "An unexpected infrastructure error occurred. Please contact ops.",
            "tracker_id": request_id
        }
    )

# ------------------------------------------------------------------
# MOCK TELEMETRY MIDDLEWARE (From Day 33)
# ------------------------------------------------------------------
@app.middleware("http")
async def inject_tracing_id(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    return response

# ------------------------------------------------------------------
# CRASH-PRONE ENDPOINTS FOR TESTING
# ------------------------------------------------------------------
@app.get("/api/v1/gpu/status")
async def check_gpu():
    return {"status": "online", "vram_available": "16GB"}

@app.get("/api/v1/gpu/simulate-oom")
async def simulate_out_of_memory():
    """Simulates a critical GPU Out-Of-Memory error."""
    raise RuntimeError("CUDA out of memory. Tried to allocate 8.50 GiB")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
