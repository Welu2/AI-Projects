from pydantic import BaseModel, Field, validator
from typing import Optional

class AIInferenceRequest(BaseModel):
    """Pydantic data validation model acting as a gateway security check."""
    model_name: str = Field(..., description="The name of the LLM or vision model to run.")
    prompt: str = Field(..., min_length=3, max_length=1000, description="The input text for inference.")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="The sampling creativity metric.")
    max_tokens: int = Field(512, gt=0, le=4096, description="Upper bound token cap.")
    stream: Optional[bool] = False

    @validator("model_name")
    def validate_allowed_models(cls, v):
        """Ensures incoming requests only execute authorized corporate clusters."""
        allowed = ["llama3", "mistral", "phi3"]
        if v.lower() not in allowed:
            raise ValueError(f"Model '{v}' is unauthorized. Allowed: {allowed}")
        return v.lower()
