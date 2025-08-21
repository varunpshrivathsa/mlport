import os
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.tenant_repo import TenantRepo
from app.schemas import Principal

SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer(auto_error=False)
tenant_repo = TenantRepo()

class TokenData(BaseModel):
    tenant_id: str
    roles: list[str] = []
    plan: str | None = None
    sub: str | None = None

def create_jwt(tenant_id: str, roles: list[str], plan: str, subject: str = "demo"):
    payload = {
        "tenant_id": tenant_id,
        "roles": roles,
        "plan": plan,
        "sub": subject,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Principal:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")

    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data = TokenData(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

    tenant = tenant_repo.get_tenant(data.tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unknown tenant")

    return Principal(
        tenant_id=data.tenant_id,
        roles=data.roles,
        plan=data.plan,
        subject=data.sub,
        metadata=tenant
    )
