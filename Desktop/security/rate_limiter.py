"""
Security Module: Rate Limiting
In-memory rate limiter for login attempts (per IP/user)
"""
import time
import threading
from collections import defaultdict
from typing import Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class RateLimitBucket:
    """Token bucket for rate limiting."""
    count: int = 0
    window_start: float = field(default_factory=time.time)
    blocked_until: float = 0


class RateLimiter:
    """
    Thread-safe rate limiter using sliding window algorithm.
    """

    def __init__(
        self,
        max_attempts: int = 5,
        window_seconds: int = 60,
        block_duration: int = 300
    ):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.block_duration = block_duration
        self._buckets: Dict[str, RateLimitBucket] = defaultdict(RateLimitBucket)
        self._lock = threading.RLock()

    def _get_bucket(self, key: str) -> RateLimitBucket:
        """Get or create bucket for key."""
        with self._lock:
            return self._buckets[key]

    def _cleanup_expired(self):
        """Remove expired buckets to prevent memory leak."""
        now = time.time()
        with self._lock:
            expired_keys = [
                k for k, v in self._buckets.items()
                if v.blocked_until > 0 and v.blocked_until < now
                and v.count == 0
            ]
            for k in expired_keys:
                del self._buckets[k]

    def check_rate_limit(self, key: str) -> Tuple[bool, Optional[int], Optional[int]]:
        """
        Check if request is allowed.

        Returns:
            (allowed, remaining_attempts, retry_after_seconds)
            - allowed: True if request allowed, False if rate limited
            - remaining_attempts: attempts left in current window
            - retry_after_seconds: seconds until next attempt allowed (if blocked)
        """
        self._cleanup_expired()

        with self._lock:
            bucket = self._buckets[key]
            now = time.time()

            # Check if currently blocked
            if bucket.blocked_until > now:
                retry_after = int(bucket.blocked_until - now) + 1
                return False, 0, retry_after

            # Reset window if expired
            if now - bucket.window_start >= self.window_seconds:
                bucket.count = 0
                bucket.window_start = now

            # Check limit
            if bucket.count >= self.max_attempts:
                # Block for block_duration
                bucket.blocked_until = now + self.block_duration
                retry_after = self.block_duration
                return False, 0, retry_after

            # Increment and allow
            bucket.count += 1
            remaining = self.max_attempts - bucket.count
            return True, remaining, None

    def reset(self, key: str):
        """Reset rate limit for a key (e.g., on successful login)."""
        with self._lock:
            if key in self._buckets:
                del self._buckets[key]

    def get_status(self, key: str) -> Dict:
        """Get current status for a key (for debugging)."""
        with self._lock:
            bucket = self._buckets.get(key)
            if not bucket:
                return {"attempts": 0, "blocked": False, "retry_after": None}

            now = time.time()
            blocked = bucket.blocked_until > now
            retry_after = int(bucket.blocked_until - now) if blocked else None

            return {
                "attempts": bucket.count,
                "max_attempts": self.max_attempts,
                "remaining": max(0, self.max_attempts - bucket.count),
                "blocked": blocked,
                "retry_after": retry_after,
                "window_reset_in": max(0, int(self.window_seconds - (now - bucket.window_start)))
            }


# Global instance for login (5 attempts per minute, 5 min block)
login_limiter = RateLimiter(
    max_attempts=5,
    window_seconds=60,
    block_duration=300
)


# --- Testing ---
if __name__ == "__main__":
    limiter = RateLimiter(max_attempts=3, window_seconds=10, block_duration=5)

    # Test normal usage
    for i in range(3):
        allowed, remaining, retry = limiter.check_rate_limit("test_user")
        assert allowed, f"Attempt {i+1} should be allowed"
        print(f"Attempt {i+1}: allowed={allowed}, remaining={remaining}")

    # 4th attempt should be blocked
    allowed, remaining, retry = limiter.check_rate_limit("test_user")
    assert not allowed, "4th attempt should be blocked"
    assert retry is not None, "Should have retry_after"
    print(f"Attempt 4: allowed={allowed}, retry_after={retry}s")

    # Different key should work
    allowed, _, _ = limiter.check_rate_limit("other_user")
    assert allowed, "Different key should not be blocked"
    print("Different key: allowed")

    # Test reset
    limiter.reset("test_user")
    allowed, _, _ = limiter.check_rate_limit("test_user")
    assert allowed, "After reset should be allowed"
    print("After reset: allowed")

    print("\n[OK] All rate limiter tests passed!")