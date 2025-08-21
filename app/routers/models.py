from fastapi import APIRouter, Depends
from app.auth import verify_jwt
from app.schemas import Principal

router = APIRouter(prefix="/v1/models", tags=["models"])

@router.get("")
def list_models(principal: Principal = Depends(verify_jwt)):
    # You can use principal.tenant_id, principal.roles etc
    return {
        "tenant": principal.tenant_id,
        "models": [{"name": "demo", "version": "1.0"}]
    }
