# tests/test_app.py
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.app import handle_request, get_request_count, clear_logs


def test_request_is_logged():
    clear_logs()
    handle_request("client_1", "/api/data")
    assert get_request_count("client_1") == 1


def test_count_respects_window():
    clear_logs()
    handle_request("client_2", "/api/data")
    time.sleep(0.01)
    count = get_request_count("client_2", window_seconds=1)
    assert count == 1


def test_unknown_client_returns_zero():
    clear_logs()
    assert get_request_count("unknown_client") == 0


if __name__ == "__main__":
    test_request_is_logged()
    test_count_respects_window()
    test_unknown_client_returns_zero()
    print("All tests passed")
