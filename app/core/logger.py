# app/core/logger.py
import json
from datetime import datetime, timezone
from typing import Any, Dict
from .request_context import get_request_id

def log(level: str, event: str, **fields: Dict[str, Any]) -> None:
    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": level.upper(),
        "event": event,
        "request_id": get_request_id(),
        **fields,
    }
    print(json.dumps(rec, separators=(",", ":")))
