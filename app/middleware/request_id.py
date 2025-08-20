# app/middleware/request_id.py
from uuid import uuid4
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..core.request_context import set_request_id, reset_request_id

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Prefer client-sent id if present (propagation), else generate one
        rid = request.headers.get("X-Request-ID") or str(uuid4())
        token = set_request_id(rid)
        try:
            request.state.request_id = rid
            response = await call_next(request)
        finally:
            reset_request_id(token)

        response.headers["X-Request-ID"] = rid
        return response
