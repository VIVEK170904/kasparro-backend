from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_stats():
    response = client.get("/stats")
    assert response.status_code == 200

    body = response.json()

    assert "total_items" in body
    assert "average_price" in body
    assert "min_price" in body
    assert "max_price" in body
