# app/core/request_context.py
from contextvars import ContextVar
from typing import Optional

_request_id_ctx: ContextVar[Optional[str]] = ContextVar("request_id", default=None)

def set_request_id(value: str):
    return _request_id_ctx.set(value)

def reset_request_id(token):
    _request_id_ctx.reset(token)

def get_request_id() -> Optional[str]:
    return _request_id_ctx.get()
