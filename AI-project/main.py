import time
import yaml
import logging
from collections import defaultdict
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

# ------------------------------------------------------------------
# 1. PLATFORM CONFIGURATION LOADER
# ------------------------------------------------------------------
def load_infra_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_infra_config()
infra_settings = config["infrastructure"]

app = FastAPI(title="Decoupled Config-Driven AI Engine")
logging.basicConfig(level=infra_settings["telemetry"]["log_level"])
logger = logging.getLogger("InfraEngine")

# ------------------------------------------------------------------
# 2. ISOLATED RATE LIMITER COMPONENT
# ------------------------------------------------------------------
class ConfiguredTokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = defaultdict(lambda: (time.time(), float(capacity)))

    def evaluate_request(self, client_ip: str) -> bool:
        now = time.time()
        last_check, tokens = self.buckets[client_ip]
        
        # Calculate refilled tokens dynamically based on config rules
        elapsed = now - last_check
        tokens = min(self.capacity, tokens + (elapsed * self.refill_rate))
        
        if tokens >= 1.0:
            self.buckets[client_ip] = (now, tokens - 1.0)
            return True # Allowed
        
        self.buckets[client_ip] = (now, tokens)
        return False # Throttled

# Instantiate bucket directly using parameters mapped from our YAML file
limiter_settings = infra_settings["rate_limiting"]
bucket_guard = ConfiguredTokenBucket(
    capacity=limiter_settings["max_tokens"], 
    refill_rate=limiter_settings["refill_rate"]
)

# ------------------------------------------------------------------
# 3. CONDITIONAL PLUGGABLE MIDDLEWARE PIPES
# ------------------------------------------------------------------
@app.middleware("http")
async def pluggable_infra_pipeline(request: Request, call_next):
    # Dynamic toggle driven entirely by changing our external YAML config
    if infra_settings["rate_limiting"]["enabled"]:
        client_ip = request.client.host or "127.0.0.1"
        
        if not bucket_guard.evaluate_request(client_ip):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"error": "Rate limit tripped via YAML policy configuration."}
            )
            
    # Trace telemetry if configured
    if infra_settings["telemetry"]["inject_client_ip"]:
        logger.info(f"[TRACE] Routing request from: {request.client.host}")
        
    return await call_next(request)

# ------------------------------------------------------------------
# CORE API ENDPOINTS
# ------------------------------------------------------------------
@app.get("/api/v1/compute")
async def run_compute():
    return {"status": "operational", "config_layer": "YAML Engine"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
