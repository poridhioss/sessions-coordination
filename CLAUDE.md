# rate-limit-lab

## Code style
- snake_case for all names
- Type annotations required on all functions
- Tests live in tests/, run with: python3 tests/test_app.py

## Architecture
- src/app.py: request handling and in-memory log
- Rate limiting logic will go in src/rate_limiter.py
- Rate limit middleware will wrap handle_request in src/app.py

## Compact Instructions
When compacting, preserve:
- Current task and next action
- Files modified this session
- Any failing test names

## Session observability
- Run /session-start at the beginning of every session
- Run /session-report before ending any session with more than 5 exchanges
- Session reports go in session-reports/ — commit them alongside code
