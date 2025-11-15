# tests/test_ccxt_integration.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from src.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_ccxt_client(monkeypatch):
    # Patch CCXTClient.fetch_ticker and fetch_ohlcv
    from src.services.ccxt_client import CCXTClient
    monkeypatch.setattr(CCXTClient, "fetch_ticker", AsyncMock(return_value={
        "symbol": "BTC/USDT", "last": 60000.0, "bid": 59999.0, "ask": 60001.0, "info": {"stub": True}
    }))
    monkeypatch.setattr(CCXTClient, "fetch_ohlcv", AsyncMock(return_value=[
        [1620000000000, 60000, 60010, 59990, 60005, 1.2],
        [1620000060000, 60005, 60015, 59995, 60010, 1.3],
    ]))
    yield

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_ticker():
    r = client.get("/market/ticker?exchange=binance&symbol=BTC/USDT")
    assert r.status_code == 200
    j = r.json()
    assert "symbol" in j and j["symbol"] == "BTC/USDT"
    assert "last" in j

def test_history():
    r = client.get("/market/history?exchange=binance&symbol=BTC/USDT&limit=2")
    assert r.status_code == 200
    j = r.json()
    assert "ohlcv" in j
    assert isinstance(j["ohlcv"], list)
