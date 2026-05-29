import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Infrastructure Middleware Guard")

# ------------------------------------------------------------------
# 1. CORS GUARDRAIL CONFIGURATION
# ------------------------------------------------------------------
# In production, never leave this as ["*"]. Define explicit origins.
ALLOWED_ORIGINS = [
    "http://localhost:3000",      # Local frontend development (React/Next.js)
    "https://streamlit.io",       # Trusted Streamlit cloud domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Restrict allowed HTTP verbs
    allow_headers=["Content-Type", "Authorization"],  # Restrict allowed headers
)

# ------------------------------------------------------------------
# 2. CUSTOM LOGGING & PERFORMANCE MIDDLEWARE
# ------------------------------------------------------------------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    
    # Pass the request down the pipeline to the endpoint
    response = await call_next(request)
    
    # Calculate execution metrics
    process_time = time.perf_counter() - start_time
    
    # Inject metrics into response headers for infrastructure monitoring
    response.headers["X-Process-Time-Seconds"] = f"{process_time:.4f}"
    
    print(f"[INFRA LOG] Path: {request.url.path} | Latency: {process_time:.4f}s")
    return response

# ------------------------------------------------------------------
# 3. API ENDPOINTS
# ------------------------------------------------------------------
@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "infrastructure": "secure"}

@app.post("/api/v1/inference")
async def run_inference(payload: dict):
    # Simulating a minor AI model inference lag
    time.sleep(0.05) 
    return {"status": "success", "output": "AI Engine Response"}

if __name__ == "__main__":
    import uvicorn
    # Run the ASGI server locally
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
