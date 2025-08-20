# app/main.py
from time import perf_counter
from fastapi import FastAPI
from .schemas import HealthResponse
from .routers import inference as inference_router
from .routers import models as models_router
from .middleware.request_id import RequestIdMiddleware

SERVICE_NAME = "mlport-api"
_start = perf_counter()

app = FastAPI(title="MLPort API Gateway", version="0.1.0", docs_url="/docs")

# ✅ add middleware
app.add_middleware(RequestIdMiddleware)

@app.get("/", summary="Service root")
def root():
    return {"message": "service is up"}

@app.get("/v1/health", response_model=HealthResponse, summary="Healthcheck")
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=SERVICE_NAME,
        uptime_sec=perf_counter() - _start,
    )

app.include_router(inference_router.router)
app.include_router(models_router.router)
