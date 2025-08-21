# app/schemas.py
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class Principal(BaseModel):
    tenant_id: str
    roles: list[str]
    plan: Optional[str]
    subject: Optional[str]
    metadata: dict

class InferenceRequest(BaseModel):
    model: str = Field(..., description="Registered model name (e.g., 'demo').")
    version: Optional[str] = Field(None, description="Model version; if omitted, uses the model's default.")
    inputs: Dict[str, Any] = Field(..., description="Model-specific input payload.")
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {"model": "demo", "version": "1.0", "inputs": {"x": [1, 2, 3]}},
                {"model": "demo", "inputs": {"x": [10, 20, 30]}},
                {"model": "demo", "version": "1.1", "inputs": {"anything": {"goes": True}}},
            ]
        },
    )

class InferenceResponse(BaseModel):
    model: str
    version: str
    latency_ms: float
    output: Dict[str, Any]
    request_id: Optional[str] = Field(None, description="Trace id for logs/metrics.")
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "model": "demo",
                    "version": "1.0",
                    "latency_ms": 0.08,
                    "output": {"sum": 6.0, "n": 3},
                    "request_id": "6f1e2d11-8d6a-4f28-a6a0-6c2c4f19f9d5",
                }
            ]
        },
    )

class ModelInfo(BaseModel):
    name: str
    versions: List[str]
    default_version: str
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"name": "demo", "versions": ["1.0", "1.1"], "default_version": "1.0"}
            ]
        }
    )

class ModelsListResponse(BaseModel):
    models: List[ModelInfo]
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "models": [
                        {"name": "demo", "versions": ["1.0", "1.1"], "default_version": "1.0"}
                    ]
                }
            ]
        }
    )

class HealthResponse(BaseModel):
    status: str
    service: str
    uptime_sec: float
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"status": "ok", "service": "mlport-api", "uptime_sec": 12.34}
            ]
        }
    )
