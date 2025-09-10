from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_status():
    resp = client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"damaged_system": "engines"}


expected_html = """<!DOCTYPE html>
<html>
<head>
    <title>Repair</title>
</head>
<body>
<div class="anchor-point">ENG-04</div>
</body>
</html>"""

def test_repair_bay_contains_anchor_point():
    resp = client.get("/repair-bay")
    assert resp.status_code == 200
    assert resp.text == expected_html


def test_teapot_returns_418():
    resp = client.post("/teapot")
    assert resp.status_code == 418
    assert resp.json() == {"detail": "I'm a teapot"}


def test_healthz_ok():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
