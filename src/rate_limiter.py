import time
from src.rate_limiter_config import DEFAULT_MAX_REQUESTS, DEFAULT_WINDOW_SECONDS


class RateLimiter:
    def __init__(
        self,
        max_requests: int = DEFAULT_MAX_REQUESTS,
        window_seconds: int = DEFAULT_WINDOW_SECONDS,
    ) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._timestamps: dict[str, list[float]] = {}

    def check(self, client_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds

        timestamps = self._timestamps.get(client_id, [])
        valid_timestamps = [ts for ts in timestamps if ts > window_start]

        return len(valid_timestamps) < self.max_requests

    def record(self, client_id: str) -> None:
        now = time.time()
        window_start = now - self.window_seconds

        timestamps = self._timestamps.get(client_id, [])
        valid_timestamps = [ts for ts in timestamps if ts > window_start]
        valid_timestamps.append(now)

        self._timestamps[client_id] = valid_timestamps