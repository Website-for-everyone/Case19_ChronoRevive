import pytest
from fastapi.testclient import TestClient
from web.app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "chronorevive_api"

def test_get_showcase():
    response = client.get("/api/showcase-models")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["models"]) >= 3
    omega = data["models"][0]
    assert "Omega" in omega["brand"]
    assert "321" in omega["caliber"]

def test_track_order_existing():
    response = client.get("/api/track-order/CR-8492")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["found"] is True
    assert data["order"]["order_id"] == "CR-8492"
    assert len(data["order"]["stages"]) == 6

def test_track_order_dynamic():
    response = client.get("/api/track-order/CR-9999")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["found"] is True
    assert data["order"]["order_id"] == "CR-9999"

def test_appraisal_request():
    payload = {
        "client_name": "Watch Collector",
        "client_contact": "@collector_vintage",
        "watch_brand": "Omega",
        "caliber": "Calibre 321",
        "vintage_decade": "1960-1970",
        "defect_description": "Watch is running 3 minutes fast per day, radium hands corroded."
    }
    response = client.post("/api/appraisal-request", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "AP-" in data["appraisal"]["ticket_id"]
    assert "₽" in data["appraisal"]["estimate_range"]

def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "CHRONOREVIVE" in response.text
    assert "escapement-canvas" in response.text
    assert "slider-divider" in response.text
    assert "track-id-input" in response.text
