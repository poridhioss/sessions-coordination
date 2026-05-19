# src/app.py
import time
from typing import Dict


_request_log: Dict[str, list] = {}


def handle_request(client_id: str, endpoint: str) -> dict:
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
