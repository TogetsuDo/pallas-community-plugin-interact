from collections import deque

from spam import record_spam_message, remember_message


def test_record_spam_message_uses_event_time_and_handles_out_of_order_events() -> None:
    timestamps = deque([10.0, 12.0])

    assert record_spam_message(timestamps, now=11.0, threshold=3, window_sec=2) is True
    assert not timestamps


def test_remember_message_deduplicates_multi_bot_delivery() -> None:
    seen: dict[tuple[int, int], float] = {}

    assert remember_message(seen, (733291779, 123), now=10.0, ttl_sec=60) is True
    assert remember_message(seen, (733291779, 123), now=11.0, ttl_sec=60) is False
    assert remember_message(seen, (733291779, 123), now=71.0, ttl_sec=60) is True
