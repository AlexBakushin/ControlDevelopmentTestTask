import time
from collections import defaultdict
from config import settings
from fastapi import HTTPException, Request


requests_map = defaultdict(list)


def rate_limit(ip: str):
    now = time.time()
    window_start = now - settings.WINDOW

    requests_map[ip] = [t for t in requests_map[ip] if t > window_start]

    if len(requests_map[ip]) >= settings.RATE_LIMIT:
        return False

    requests_map[ip].append(now)
    return True