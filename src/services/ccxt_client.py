# src/services/ccxt_client.py
import ccxt.async_support as ccxt
import asyncio
from typing import Any, Dict, List, Optional
from src.utils.errors import ExchangeNotSupportedError

DEFAULT_TIMEOUT = 10_000  # ms

class CCXTClient:
    def __init__(self):
        self._exchanges: Dict[str, ccxt.Exchange] = {}
        self._lock = asyncio.Lock()

    async def _get_exchange(self, exchange_id: str) -> ccxt.Exchange:
        exchange_id = exchange_id.lower()
        async with self._lock:
            if exchange_id in self._exchanges:
                return self._exchanges[exchange_id]
            try:
                ex_cls = getattr(ccxt, exchange_id)
            except AttributeError:
                raise ExchangeNotSupportedError(f"Exchange '{exchange_id}' is not supported by CCXT")
            ex = ex_cls({
                "enableRateLimit": True,
                "timeout": DEFAULT_TIMEOUT,
            })
            # some exchanges warn on load_markets; we try to load markets lazily
            try:
                await ex.load_markets()
            except Exception:
                # not fatal; some exchanges don't allow this without API keys
                pass
            self._exchanges[exchange_id] = ex
            return ex

    async def fetch_ticker(self, exchange_id: str, symbol: str) -> Dict[str, Any]:
        ex = await self._get_exchange(exchange_id)
        try:
            ticker = await asyncio.wait_for(ex.fetch_ticker(symbol), timeout=10)
            return ticker
        except Exception as e:
            # wrap common errors into ExchangeNotSupportedError or re-raise
            raise

    async def fetch_ohlcv(
        self,
        exchange_id: str,
        symbol: str,
        timeframe: str = "1m",
        since: Optional[int] = None,
        limit: int = 100,
    ) -> List[List[Any]]:
        ex = await self._get_exchange(exchange_id)
        try:
            ohlcv = await asyncio.wait_for(
                ex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit),
                timeout=20,
            )
            return ohlcv
        except Exception as e:
            raise

    async def close(self) -> None:
        for ex in list(self._exchanges.values()):
            try:
                await ex.close()
            except Exception:
                pass
        self._exchanges.clear()
