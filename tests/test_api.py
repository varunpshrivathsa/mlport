from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/v1/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "mlport-api"
    assert isinstance(body["uptime_sec"], (int, float))

def test_models_list():
    r = client.get("/v1/models")
    assert r.status_code == 200
    data = r.json()
    assert "models" in data and isinstance(data["models"], list)
    assert any(m["name"] == "demo" for m in data["models"])

def test_infer_ok():
    payload = {"model": "demo", "version": "1.0", "inputs": {"x": [1, 2, 3]}}
    r = client.post("/v1/infer", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["output"]["sum"] == 6.0
    assert body["output"]["n"] == 3
    assert body.get("request_id")
    assert "X-Request-ID" in r.headers
    assert r.headers["X-Request-ID"] == body["request_id"]

def test_infer_bad_model_404():
    r = client.post("/v1/infer", json={"model": "nope", "inputs": {"x": [1]}})
    assert r.status_code == 404
    assert "detail" in r.json()

def test_infer_bad_version_400():
    r = client.post("/v1/infer", json={"model": "demo", "version": "9.9", "inputs": {"x": [1]}})
    assert r.status_code == 400

def test_infer_422_missing_inputs():
    r = client.post("/v1/infer", json={"model": "demo"})
    assert r.status_code == 422

def test_request_id_propagation():
    headers = {"X-Request-ID": "test-corr-123"}
    r = client.post("/v1/infer", headers=headers, json={"model": "demo", "inputs": {"x": [7]}})
    assert r.status_code == 200
    assert r.headers["X-Request-ID"] == "test-corr-123"
    assert r.json()["request_id"] == "test-corr-123"
