# app/routers/inference.py
from time import perf_counter
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, Response, Request, Depends

from ..schemas import InferenceRequest, InferenceResponse, Principal
from ..auth import verify_jwt
from ..core.logger import log  # optional

router = APIRouter(prefix="/v1", tags=["inference"])

_DEFAULTS = {"demo": {"versions": ["1.0", "1.1"], "default_version": "1.0"}}

def _mock_predict(req: InferenceRequest) -> Dict[str, Any]:
    inputs = req.inputs
    if "x" in inputs and isinstance(inputs["x"], list) and all(isinstance(v, (int, float)) for v in inputs["x"]):
        xs: List[float] = [float(v) for v in inputs["x"]]
        return {"sum": sum(xs), "n": len(xs)}
    return {"echo": inputs}

@router.post(
    "/infer",
    response_model=InferenceResponse,
    summary="Run inference (stub, auth protected)",
    responses={
        200: {
            "headers": {
                "X-Request-ID": {
                    "description": "Trace id for logs/metrics",
                    "schema": {"type": "string"}
                }
            }
        }
    },
)
def infer(
    req: InferenceRequest,
    request: Request,
    response: Response,
    principal: Principal = Depends(verify_jwt)  # 🔑 NEW: Require valid tenant
) -> InferenceResponse:
    meta = _DEFAULTS.get(req.model)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Unknown model '{req.model}'")

    version = req.version or meta["default_version"]
    if version not in meta["versions"]:
        raise HTTPException(status_code=400, detail=f"Version '{version}' not available for '{req.model}'")

    t0 = perf_counter()
    output = _mock_predict(req)
    latency_ms = (perf_counter() - t0) * 1000.0

    rid = getattr(request.state, "request_id", None)

    try:
        log("info", "infer.ok", model=req.model, version=version,
            latency_ms=latency_ms, tenant=principal.tenant_id)
    except Exception:
        pass

    return InferenceResponse(
        model=req.model,
        version=version,
        latency_ms=latency_ms,
        output=output,
        request_id=rid,
    )
