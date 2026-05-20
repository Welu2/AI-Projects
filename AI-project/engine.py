import asyncio
import json
import os

CONFIG_FILE = "system_config.json"

def save_config(operator_name, server_multiplier):
    """Saves the operator configurations to a JSON file."""
    data = {
        "operator": operator_name,
        "multiplier": server_multiplier
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    """Loads configurations if they exist, otherwise returns defaults."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"operator": "Default Alpha", "multiplier": 12.5}

def get_system_greeting(operator_name):
    """Returns a welcome message for the infrastructure hub."""
    return f"Welcome back, Operator {operator_name}! System online."

def compute_server_load(multiplier):
    """Simulates or calculates the current server load based on the multiplier."""
    # Placeholder logic: adjust this based on your actual business logic
    import random
    base_load = random.uniform(10.0, 30.0)
    return round(base_load * multiplier, 2)

async def simulate_heavy_ai_job(job_id: str, steps: int = 5):
    """Simulates a heavy, non-blocking background AI pipeline job."""
    for i in range(1, steps + 1):
        # Instead of time.sleep() which freezes the app, 
        # asyncio.sleep allows other tasks to run simultaneously
        await asyncio.sleep(0.8) 
        yield f"Job {job_id}: Processing step {i}/{steps}..."
    yield f"Job {job_id}: Pipeline execution complete! 🎉"