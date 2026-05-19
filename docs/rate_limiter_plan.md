# Rate Limiter Implementation Plan

## Decision: sliding window algorithm
Chosen over fixed window to prevent burst abuse at window boundaries.

## Implementation plan
1. src/rate_limiter.py — RateLimiter class with check() and record()
2. src/app.py — wrap handle_request with rate limit check
3. Config: 100 requests per 60-second window per client

## Files relevant to implementation
- src/app.py: _request_log already tracks timestamps per client
- tests/test_app.py: add rate limit tests alongside existing tests
