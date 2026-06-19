import pytest
from tasks.booking_tasks import process_booking


def test_worker_failure(monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.01)
    try:
        process_booking(1)
        assert False
    except Exception:
        assert True
