from fastapi import APIRouter
from ..schemas import ModelInfo, ModelsListResponse

router = APIRouter(prefix="/v1", tags=["models"])

_MODELS = [
    ModelInfo(name="demo", versions=["1.0", "1.1"], default_version="1.0")
]

@router.get("/models", response_model=ModelsListResponse, summary="List available models (stub)")
def list_models() -> ModelsListResponse:
    return ModelsListResponse(models=_MODELS)
