# MCP Server (Python) — Crypto Market Connector Provider
Overview

This project is a Python-based Market Connector Provider (MCP) server that fetches real-time and historical cryptocurrency market data using FastAPI, CCXT, and WebSockets.

I built this project to understand how real trading platforms and analytics dashboards fetch, aggregate, and stream live data. Instead of just reading theory, I wanted to experience how real-time systems behave in practice — rate limits, network delays, caching, websocket streaming, and backend architecture.

🚀 What This Project Does

This backend provides:

✔️ Real-Time Crypto Prices

Fetch live tickers from exchanges (Binance, Kraken, etc.)

GET /market/ticker?exchange=binance&symbol=BTC/USDT

✔️ Historical OHLCV Candlesticks

Get candles (open, high, low, close, volume) for charting.

GET /market/history?exchange=binance&symbol=BTC/USDT&limit=100

✔️ Live Streaming via WebSockets

Receive continuous price updates every few seconds.

ws://localhost:8000/ws/realtime?exchange=binance&symbol=BTC/USDT

✔️ Caching Layer

A small in-memory TTL cache (Redis-ready if needed).

✔️ Clean Architecture

services/ for CCXT wrapper
utils/ for caching & errors
main.py for API routing

✔️ Mocked Tests (pytest)

All CCXT calls are mocked → tests run fast & offline.

💡 Why I Built This

I wanted to challenge myself with a backend system that feels real, not a simple CRUD API.

Crypto market data is perfect for learning because it’s:

Real-time

Fast-moving

Unpredictable

API-driven

Used everywhere (finance, analytics, dashboards, bots)

This project helped me practice:

🧠 Backend engineering

Designing structured, testable modules.

⚡ Real-time systems

Learning how continuous data streaming works.

🧪 Practical testing

Mocking external APIs (CCXT) so tests don’t rely on the network.

🐳 Deployable backend skills

Docker, Docker Compose, cloud deployment readiness.

This is exactly the type of engineering work I want to contribute to during my internship.

🛠️ Tech Stack

FastAPI (web framework)

CCXT (exchange data layer)

WebSockets (live streaming)

Cachetools TTLCache (lightweight caching)

Pytest (unit testing with mocks)

Docker (deployment-ready)

Redis (optional) for shared caching

📁 Project Structure
mcp-server/
│── src/
│   ├── main.py
│   ├── services/
│   │   └── ccxt_client.py
│   ├── utils/
│   │   ├── cache.py
│   │   └── errors.py
│   └── models.py
│
├── tests/
│   ├── test_api.py
│   └── test_ccxt_integration.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

⚙️ How to Run the Project
1️⃣ Create a virtual environment
python -m venv .venv


Activate it:

Windows PowerShell:

.\.venv\Scripts\Activate.ps1


Mac/Linux:

source .venv/bin/activate

2️⃣ Install requirements
pip install -r requirements.txt

3️⃣ Start the server
uvicorn src.main:app --reload --port 8000


Server will run at:

👉 http://127.0.0.1:8000

👉 API Docs: http://127.0.0.1:8000/docs

🧪 Running Tests
pytest -q


All CCXT calls are mocked — tests do NOT hit real exchanges.

🐳 Docker Support
Run server + Redis:
docker-compose up --build


Server → http://localhost:8000

Redis → redis://localhost:6379

🎨 Bonus: Frontend Dashboard (React + Vite)

This backend is paired with a clean dashboard that shows:

Live prices (via WebSocket)

Historical candlestick chart

Exchange/symbol selection

If you want the downloadable ZIP, just tell me:

👉 “Generate dashboard ZIP”

🎯 What I Learned

Building this taught me about:

Real-time streaming patterns

Handling external API unreliability

Integrating async services

Testing asynchronous code

Clean service-oriented backend design

Dockerizing and preparing for cloud deployment

Most importantly, I learned how real market-data systems work under the hood — something I couldn’t have learned from tutorials alone.

🤝 Future Improvements

Native Binance WebSocket stream (tick-by-tick updates)

Redis-backed caching layer

Historical database storage (PostgreSQL)

Alerts/notifications system

Production deploy to Render or Railway

❤️ Why This Project Matters to Me

I built this because I genuinely enjoy systems that feel “alive” — streaming, updating, reacting.
Working on this gave me confidence that I can design real backend systems that actually serve live data, not just static CRUD endpoints.

This aligns perfectly with the kind of engineering work I want to explore as an intern
