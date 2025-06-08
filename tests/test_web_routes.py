import pytest
import requests_mock

from app import app
from app.db.sqlite_handler import delete_symbol


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_add_symbol(client):
    delete_symbol("MBB")  # Đảm bảo xóa trước
    response = client.post("/add", data={
        "symbol": "MBB",
        "buy_price": "20000",
        "sell_price": "25000",
        "profit_loss": "25"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"MBB" in response.data


def test_refresh_symbol(client):
    # Giả lập giá API cho Vietstock
    with requests_mock.Mocker() as m:
        m.post(requests_mock.ANY, json={"LastPrice": 21123})

        response = client.get("/refresh/MBB", follow_redirects=True)
        assert response.status_code == 200
        # assert b"MBB" in response.data or f"Đã cập nhật" in response.data


def test_delete_symbol(client):
    response = client.get("/delete/MBB", follow_redirects=True)
    assert response.status_code == 200
    # assert b"MBB" not in response.data
