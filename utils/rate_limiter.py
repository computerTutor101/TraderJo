# utils/rate_limiter.py

import time

class RateLimiter:
    def __init__(self, max_calls_per_minute=1200):
        self.max_calls = max_calls_per_minute
        self.calls = []
    
    def record_call(self):
        now = time.time()
        self.calls.append(now)
        self._cleanup(now)

    def _cleanup(self, now):
        # Only keep timestamps from the last 60 seconds
        self.calls = [t for t in self.calls if now - t < 60]

    def is_safe(self):
        now = time.time()
        self._cleanup(now)
        return len(self.calls) < self.max_calls

    def wait_if_unsafe(self):
        while not self.is_safe():
            print("⏳ Waiting for rate limit to clear...")
            time.sleep(1)
