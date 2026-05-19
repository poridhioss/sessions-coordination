# src/app.py
import time
from typing import Dict

from src.rate_limiter import RateLimiter
from src.rate_limiter_config import DEFAULT_MAX_REQUESTS, DEFAULT_WINDOW_SECONDS


rate_limiter = RateLimiter(
    max_requests=DEFAULT_MAX_REQUESTS,
    window_seconds=DEFAULT_WINDOW_SECONDS
)

_request_log: Dict[str, list] = {}


def handle_request(client_id: str, endpoint: str) -> dict:
    if not rate_limiter.check(client_id):
        return {"status": "rate_limited"}
    rate_limiter.record(client_id)
    timestamp = time.time()
    if client_id not in _request_log:
        _request_log[client_id] = []
    _request_log[client_id].append({"endpoint": endpoint, "timestamp": timestamp})
    return {"status": "ok", "client_id": client_id, "endpoint": endpoint}


def get_request_count(client_id: str, window_seconds: int = 60) -> int:
    if client_id not in _request_log:
        return 0
    cutoff = time.time() - window_seconds
    return sum(1 for r in _request_log[client_id] if r["timestamp"] > cutoff)


def clear_logs():
    _request_log.clear()
