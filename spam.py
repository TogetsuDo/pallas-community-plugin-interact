from collections import deque


def remember_message(
    seen_messages: dict[tuple[int, int], float],
    message_key: tuple[int, int],
    *,
    now: float,
    ttl_sec: float,
) -> bool:
    cutoff = now - ttl_sec
    for key, seen_at in tuple(seen_messages.items()):
        if seen_at < cutoff:
            seen_messages.pop(key, None)
    if message_key in seen_messages:
        return False
    seen_messages[message_key] = now
    return True


def record_spam_message(
    timestamps: deque[float],
    *,
    now: float,
    threshold: int,
    window_sec: int,
) -> bool:
    timestamps.append(now)
    ordered = sorted(timestamps)
    cutoff = ordered[-1] - window_sec
    timestamps.clear()
    timestamps.extend(timestamp for timestamp in ordered if timestamp >= cutoff)
    if len(timestamps) < threshold or not any(
        timestamps[index + threshold - 1] - timestamps[index] <= window_sec
        for index in range(len(timestamps) - threshold + 1)
    ):
        return False
    timestamps.clear()
    return True
