from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_data_endpoint():
    response = client.get("/data?limit=10&offset=0")
    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert "total" in body
    assert body["limit"] == 10
    assert body["offset"] == 0
    assert isinstance(body["data"], list)
