import time
import uuid
import logging
import json
from fastapi import FastAPI, Request

app = FastAPI(title="AI Infrastructure Telemetry & Tracing")

# Configure system logger to output clean text or structures
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI_Platform")

# ------------------------------------------------------------------
# TRACING MIDDLEWARE (CORRELATION ID)
# ------------------------------------------------------------------
@app.middleware("http")
async def add_telemetry_tracing(request: Request, call_next):
    # Check if upstream service already passed an ID; if not, generate one
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    
    # Store ID on request state so endpoints can access it if needed
    request.state.request_id = request_id
    
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    
    # Pass the ID back to the client/frontend for debugging loops
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Runtime-Duration"] = f"{duration:.4f}s"
    
    # Structured JSON log payload for modern infrastructure collectors
    log_payload = {
        "timestamp": time.time(),
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_sec": round(duration, 4)
    }
    
    # Output as a single line JSON string
    logger.info(json.dumps(log_payload))
    return response

# ------------------------------------------------------------------
# ENDPOINTS
# ------------------------------------------------------------------
@app.get("/api/v1/predict")
async def mock_predict(request: Request):
    # Accessing the middleware context safely inside an endpoint
    current_id = getattr(request.state, "request_id", "unknown")
    return {
        "msg": "Inference completed", 
        "tracked_by": current_id
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
