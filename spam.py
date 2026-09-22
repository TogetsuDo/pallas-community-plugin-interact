from collections import deque


def record_spam_message(
    timestamps: deque[float],
    *,
    now: float,
    threshold: int,
    window_sec: int,
) -> bool:
    cutoff = now - window_sec
    while timestamps and timestamps[0] < cutoff:
        timestamps.popleft()
    timestamps.append(now)
    if len(timestamps) < threshold:
        return False
    timestamps.clear()
    return True
