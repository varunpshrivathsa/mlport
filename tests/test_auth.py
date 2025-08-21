import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import create_jwt

client = TestClient(app)

def test_no_token():
    r = client.get("/v1/models")
    assert r.status_code == 401

def test_invalid_token():
    headers = {"Authorization": "Bearer invalid.token"}
    r = client.get("/v1/models", headers=headers)
    assert r.status_code == 403

def test_unknown_tenant(monkeypatch):
    token = create_jwt("ghost", ["invoker"], "free")

    # Monkeypatch TenantRepo to return None
    from app import auth
    monkeypatch.setattr(auth.tenant_repo, "get_tenant", lambda _: None)

    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/v1/models", headers=headers)
    assert r.status_code == 403

def test_valid_tenant(monkeypatch):
    token = create_jwt("acme", ["invoker"], "pro")

    from app import auth
    monkeypatch.setattr(auth.tenant_repo, "get_tenant", lambda _: {"tenant_id": "acme", "plan": "pro"})

    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/v1/models", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["tenant"] == "acme"
