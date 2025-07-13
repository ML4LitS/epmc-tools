import time
import requests
from functools import wraps

class RateLimiter:
    """
    Token-bucket rate limiter to throttle requests.
    """
    def __init__(self, rate: float, per: float):
        self._capacity = rate
        self._tokens = rate
        self._fill_rate = rate / per
        self._timestamp = time.monotonic()

    def acquire(self):
        now = time.monotonic()
        elapsed = now - self._timestamp
        self._timestamp = now
        self._tokens = min(self._capacity, self._tokens + elapsed * self._fill_rate)
        if self._tokens < 1:
            to_wait = (1 - self._tokens) / self._fill_rate
            time.sleep(to_wait)
            self._tokens = 0
        else:
            self._tokens -= 1

def retry_on_failure(max_attempts: int = 3, backoff: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = backoff
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
                    delay *= 2
        return wrapper
    return decorator

class BaseClient:
    """
    Base client for Europe PMC APIs.
    """
    def __init__(self, email: str = None, tool: str = None, rate_limit: float = 10.0):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        })
        self.email = email
        self.tool = tool
        self.rate_limiter = RateLimiter(rate_limit, 1)

    def _build_params(self, extra: dict = None) -> dict:
        params = {"format": "json"}
        if self.email:
            params["email"] = self.email
        if self.tool:
            params["tool"] = self.tool
        if extra:
            params.update(extra)
        return params

    @retry_on_failure(max_attempts=3, backoff=1)
    def _get(self, url: str, params: dict = None) -> dict:
        self.rate_limiter.acquire()
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    @retry_on_failure(max_attempts=3, backoff=1)
    def _get_text(self, url: str, params: dict = None) -> str:
        self.rate_limiter.acquire()
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.text
