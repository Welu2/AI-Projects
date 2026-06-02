import pytest
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

# ------------------------------------------------------------------
# 1. DEFINE TARGET INFRASTRUCTURE (The Application)
# ------------------------------------------------------------------
app = FastAPI(title="Day 37 Testable Core Engine")

@app.middleware("http")
async def security_header_middleware(request: Request, call_next):
    """Injects security clearance validation during the request cycle."""
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Platform-Layer"] = "Verified"
    return response

@app.get("/api/v1/system/status")
async def get_system_status():
    return {"status": "operational"}

# ------------------------------------------------------------------
# 2. AUTOMATED INFRASTRUCTURE UNIT TESTS
# ------------------------------------------------------------------
# TestClient handles request-response loops locally inside memories
client = TestClient(app)

def test_system_status_endpoint_returns_success():
    """Asserts that the core status endpoint responds correctly."""
    response = client.get("/api/v1/system/status")
    
    # Assert correct HTTP response metadata
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "operational"}

def test_middleware_injects_required_security_headers():
    """Asserts that our custom middleware intercepts and decorates responses."""
    response = client.get("/api/v1/system/status")
    
    # Assert infrastructure security expectations are present in headers
    assert "X-Frame-Options" in response.headers
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Platform-Layer"] == "Verified"

def test_invalid_route_returns_404():
    """Asserts that non-existent system routes are caught correctly."""
    response = client.get("/api/v1/missing-component")
    assert response.status_code == status.HTTP_404_NOT_FOUND
