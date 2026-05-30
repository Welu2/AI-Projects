import time
from collections import defaultdict
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI(title="AI Infrastructure Rate Limiting Engine")

# ------------------------------------------------------------------
# TOKEN BUCKET RATE LIMITER STORAGE
# ------------------------------------------------------------------
class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity          # Maximum burst tokens allowed
        self.refill_rate = refill_rate      # Tokens added per second
        # Storage schema: { ip_address: (last_updated_timestamp, current_tokens) }
        self.buckets = defaultdict(lambda: (time.time(), float(capacity)))

    def is_rate_limited(self, client_ip: str) -> bool:
        now = time.time()
        last_check, tokens = self.buckets[client_ip]

        # 1. Calculate how many tokens accumulated since the last request
        elapsed = now - last_check
        refilled_tokens = tokens + (elapsed * self.refill_rate)
        
        # 2. Cap the tokens at maximum bucket capacity
        tokens = min(self.capacity, refilled_tokens)
        
        # 3. Evaluate if the client has enough tokens to execute the request
        if tokens >= 1.0:
            self.buckets[client_ip] = (now, tokens - 1.0)
            return False  # Request allowed
        
        # Save the current state even if rejected to track elapsed time accurately
        self.buckets[client_ip] = (now, tokens)
        return True  # Rate limited!

# Instantiate limiter: Max 3 tokens, refills 0.5 tokens/sec (1 token every 2 seconds)
limiter = TokenBucketLimiter(capacity=3, refill_rate=0.5)

# ------------------------------------------------------------------
# RATE LIMITER MIDDLEWARE
# ------------------------------------------------------------------
@app.middleware("http")
async def rate_limit_guardrail(request: Request, call_next):
    client_ip = request.client.host or "127.0.0.1"
    
    # Check if this IP address has exceeded its operational thresholds
    if limiter.is_rate_limited(client_ip):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "success": False,
                "error_code": "RATE_LIMIT_EXCEEDED",
                "message": "Too many requests to the AI engine. Please slow down.",
                "retry_after_seconds": 2.0
            },
            headers={"Retry-After": "2"}
        )
        
    return await call_next(request)

# ------------------------------------------------------------------
# CORE API ENDPOINTS
# ------------------------------------------------------------------
@app.get("/api/v1/llm/generate")
async def generate_text():
    return {"status": "success", "data": "Tokens computed successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
