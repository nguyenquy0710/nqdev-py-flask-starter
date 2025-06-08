import pytest
import requests_mock

from app import app

MOCK_DATASET = {
    "dataset": [
        ["2024-06-01T10:00:00.000000Z", 21.1],
        ["2024-06-01T10:01:00.000000Z", 21.2],
        ["2024-06-01T10:02:00.000000Z", 21.3],
    ]
}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_chart_endpoint(client):
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, json=MOCK_DATASET)

        response = client.get("/api/chart/MBB")
        assert response.status_code == 200
        json_data = response.get_json()

        assert "timestamps" in json_data
        assert "prices" in json_data
        assert len(json_data["prices"]) == 3
