import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_db_connection():
    response = client.get("/test-db")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["result"] is not None