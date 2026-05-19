# tests/test_rate_limiter.py
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.rate_limiter import RateLimiter
from src.rate_limiter_config import DEFAULT_MAX_REQUESTS, DEFAULT_WINDOW_SECONDS
from src.app import handle_request, clear_logs


def test_new_client_not_rate_limited_on_first_request():
    """A new client is not rate limited on first request."""
    clear_logs()
    rate_limiter = RateLimiter(max_requests=DEFAULT_MAX_REQUESTS, window_seconds=DEFAULT_WINDOW_SECONDS)
    result = rate_limiter.check("new_client")
    assert result is True


def test_client_exceeding_limit_is_rejected():
    """A client that exceeds DEFAULT_MAX_REQUESTS in the window is rejected."""
    clear_logs()
    rate_limiter = RateLimiter(max_requests=DEFAULT_MAX_REQUESTS, window_seconds=DEFAULT_WINDOW_SECONDS)
    client_id = "overflow_client"
    for _ in range(DEFAULT_MAX_REQUESTS):
        rate_limiter.record(client_id)
    # Next request should be rejected
    result = rate_limiter.check(client_id)
    assert result is False


def test_check_returns_true_for_allowed_false_for_rejected():
    """check() returns True for allowed requests, False for rejected."""
    clear_logs()
    rate_limiter = RateLimiter(max_requests=2, window_seconds=DEFAULT_WINDOW_SECONDS)
    client_id = "test_client"
    # First request allowed
    assert rate_limiter.check(client_id) is True
    rate_limiter.record(client_id)
    # Second request allowed
    assert rate_limiter.check(client_id) is True
    rate_limiter.record(client_id)
    # Third request rejected
    assert rate_limiter.check(client_id) is False


def test_requests_outside_window_do_not_count():
    """Requests outside DEFAULT_WINDOW_SECONDS do not count toward the limit."""
    clear_logs()
    rate_limiter = RateLimiter(max_requests=2, window_seconds=1)
    client_id = "window_client"
    # Make 2 requests to hit the limit
    rate_limiter.record(client_id)
    rate_limiter.record(client_id)
    # Should be rejected
    assert rate_limiter.check(client_id) is False
    # Wait for window to pass
    time.sleep(1.1)
    # Now should be allowed again
    assert rate_limiter.check(client_id) is True


if __name__ == "__main__":
    test_new_client_not_rate_limited_on_first_request()
    test_client_exceeding_limit_is_rejected()
    test_check_returns_true_for_allowed_false_for_rejected()
    test_requests_outside_window_do_not_count()
    print("All rate limiter tests passed")