# src/main.py
from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect, HTTPException
import asyncio
from src.services.ccxt_client import CCXTClient
from src.utils.cache import TTLCacheWrapper
from src.utils.errors import ExchangeNotSupportedError
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI(title="MCP Server - Crypto Market Connector Provider")

client = CCXTClient()
cache = TTLCacheWrapper(maxsize=2048, ttl=10)  # short TTL for demo; raise as needed

@app.on_event("shutdown")
async def shutdown_event():
    await client.close()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/market/ticker")
async def get_ticker(symbol: str = Query(..., example="BTC/USDT"), exchange: str = Query("binance")):
    key = f"ticker:{exchange}:{symbol}"
    cached = cache.get(key)
    if cached:
        return cached
    try:
        data = await client.fetch_ticker(exchange, symbol)
    except ExchangeNotSupportedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # return a consistent error to the client and log
        raise HTTPException(status_code=502, detail=f"Failed to fetch ticker: {str(e)}")
    cache.set(key, data)
    return data

@app.get("/market/history")
async def get_history(
    symbol: str = Query(..., example="BTC/USDT"),
    exchange: str = Query("binance"),
    since: Optional[int] = Query(None, description="Unix ms timestamp to start from"),
    limit: int = Query(100, ge=1, le=1000),
):
    key = f"history:{exchange}:{symbol}:{since}:{limit}"
    cached = cache.get(key)
    if cached:
        return cached

    try:
        data = await client.fetch_ohlcv(exchange, symbol, since=since, limit=limit)
    except ExchangeNotSupportedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch history: {str(e)}")

    response = {
        "exchange": exchange,
        "symbol": symbol,
        "since": since,
        "limit": limit,
        "ohlcv": data,
    }

    cache.set(key, response)
    return response


@app.websocket("/ws/realtime")
async def ws_realtime(websocket: WebSocket, exchange: str = Query("binance"), symbol: str = Query("BTC/USDT")):
    await websocket.accept()
    try:
        while True:
            try:
                data = await client.fetch_ticker(exchange, symbol)
            except Exception as e:
                await websocket.send_json({"event": "error", "message": str(e)})
                await asyncio.sleep(2)
                continue
            await websocket.send_json({"event": "ticker", "data": data})
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        return
    except Exception:
        try:
            await websocket.close()
        except Exception:
            pass


