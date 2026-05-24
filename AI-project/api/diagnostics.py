from fastapi import APIRouter, HTTPException, status, Depends 
from datetime import datetime
from api.models import AIInferenceRequest  , DBInferenceJob

from sqlalchemy.orm import Session
from database import get_db, engine, Base
  # Import our DB model

# 2. Create the physical tables when the app runs (runs on initialization)
Base.metadata.create_all(bind=engine)


# 1. Create an isolated router for infrastructure metrics
router = APIRouter(
    prefix="/infrastructure",
    tags=["Infrastructure Diagnostics"]
)

@router.get("/status")
async def get_system_status():
    """Fetches real-time status updates from the cluster node."""
    return {
        "node_status": "OPERATIONAL",
        "active_threads": 16,
        "last_health_check": datetime.utcnow().isoformat()
    }

@router.get("/metrics")
async def get_cluster_metrics():
    """Simulates raw compute resource metrics."""
    return {
        "gpu_vram_usage_gb": 4.2,
        "network_throughput_mbps": 850.5,
        "cluster_health_score": 0.99
    }
@router.post("/inference", status_code=status.HTTP_201_CREATED)
async def dispatch_inference_job(payload: AIInferenceRequest):
    """Processes incoming AI job payloads after strict Pydantic parsing."""
    # If the payload passes the Pydantic check, it arrives safely here as a Python object
    return {
        "status": "QUEUED",
        "assigned_node": "GPU-CLUSTER-EPSILON",
        "received_at": datetime.utcnow().isoformat(),
        "parsed_configuration": {
            "model": payload.model_name,
            "tokens_allocated": payload.max_tokens,
            "sampling_temp": payload.temperature
        }
    }


# 3. Update the POST route to use the database dependency
@router.post("/inference", status_code=status.HTTP_201_CREATED)
async def dispatch_inference_job(payload: AIInferenceRequest, db: Session = Depends(get_db)):
    """Validates data via Pydantic, converts it, and saves it permanently to SQLite."""
    
    # Create an instance of our SQLAlchemy DB model using the payload data
    new_job = DBInferenceJob(
        model_name=payload.model_name,
        prompt=payload.prompt,
        temperature=payload.temperature,
        max_tokens=payload.max_tokens
    )
    
    # Commit the transaction to the database
    db.add(new_job)
    db.commit()
    db.refresh(new_job) # Fetch the generated auto-increment id from SQL
    
    return {
        "status": "DATABASE_PERSISTED",
        "job_id": new_job.id,
        "saved_record": {
            "model": new_job.model_name,
            "prompt_length": len(new_job.prompt),
            "completed_flag": new_job.is_completed
        }
    }

# Ensure DBInferenceJob is imported at the top (already done on Day 27)

@router.get("/jobs", status_code=status.HTTP_200_OK)
async def get_all_inference_jobs(limit: int = 10, db: Session = Depends(get_db)):
    """Fetches the latest execution logs from the infrastructure database."""
    # query(DBInferenceJob) tells SQLAlchemy which table to scan
    # .limit() ensures our server doesn't crash if the database has millions of rows
    jobs = db.query(DBInferenceJob).limit(limit).all()
    return {
        "total_fetched": len(jobs),
        "cluster_jobs": jobs
    }
@router.get("/jobs/{job_id}", status_code=status.HTTP_200_OK)
async def get_single_job(job_id: int, db: Session = Depends(get_db)):
    """Retrieves a single target infrastructure job record by its Primary Key."""
    # .filter() acts as the SQL 'WHERE id = job_id' clause
    job = db.query(DBInferenceJob).filter(DBInferenceJob.id == job_id).first()
    
    # Error Validation Bouncer: If the client asks for an ID that doesn't exist, block them!
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inference job with ID {job_id} was not found on this cluster node."
        )
        
    return {
        "search_status": "FOUND",
        "job_details": job
    }
