import json
from app import create_app


def test_healthz():
    app = create_app()
    client = app.test_client()
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_delete_aws(monkeypatch):
    app = create_app()
    client = app.test_client()

    def fake_delete(bucket, key):
        return {"bucket": bucket, "key": key}

    monkeypatch.setattr("app.aws_delete.delete_object", fake_delete)
    r = client.post("/delete/aws", json={"bucket": "b", "key": "k"})
    assert r.status_code == 200
    body = r.get_json()
    assert body["status"] == "success"
    assert body["bucket"] == "b"
    assert body["key"] == "k"


def test_delete_azure(monkeypatch):
    app = create_app()
    client = app.test_client()

    def fake_delete(container, blob):
        return {"container": container, "blob": blob}

    monkeypatch.setattr("app.azure_delete.delete_blob", fake_delete)
    r = client.post("/delete/azure", json={"container": "c", "blob": "f"})
    assert r.status_code == 200
    body = r.get_json()
    assert body["status"] == "success"
    assert body["container"] == "c"
    assert body["blob"] == "f"
