import time
import threading
from datetime import datetime, timedelta


class Request:
    def __init__(self, client_id, path, timestamp=None):
        self.client_id = client_id
        self.path = path
        # default to "now" if not provided
        self.timestamp = timestamp or datetime.now()


class Response:
    def __init__(self, status_code, error=None):
        self.status_code = status_code
        self.error = error


class BackendClient:
    def call(self, path: str):
        raise NotImplementedError


class MockBackend(BackendClient):
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    def call(self, path: str):
        time.sleep(0.01)  # simulate latency
        if self.should_fail:
            raise Exception("backend error")


class APIGateway:
    def __init__(self, backend: BackendClient):
        self.backend = backend
        self.client_requests = {}  # client_id -> list[datetime]
        self.rate_limit_count = 10
        self.rate_limit_window = timedelta(seconds=10)

        # circuit breaker
        self.failure_count = 0
        self.circuit_open = False
        self.circuit_open_time = None
        self.failure_threshold = 3
        self.recovery_timeout = timedelta(seconds=5)

        self.mu = threading.Lock()

    def handle_request(self, req: Request) -> Response:
        now = req.timestamp  # always use provided request timestamp

        with self.mu:
            # Track request timestamps for client
            requests = self.client_requests.get(req.client_id, [])
            cutoff = now - self.rate_limit_window
            requests = [ts for ts in requests if ts > cutoff]
            requests.append(req.timestamp)   # record every request
            self.client_requests[req.client_id] = requests

            # Rate limiting check
            if len(requests) > self.rate_limit_count:
                return Response(429, error=Exception("rate limited"))

            # Circuit breaker check
            if self.circuit_open:
                if now - self.circuit_open_time > self.recovery_timeout:
                    # allow trial request
                    self.circuit_open = False
                    self.failure_count = 0
                else:
                    return Response(503, error=Exception("circuit open"))

        # Backend call outside lock
        try:
            self.backend.call(req.path)
            with self.mu:
                self.failure_count = 0
            return Response(200)
        except Exception as e:
            with self.mu:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.circuit_open = True
                    self.circuit_open_time = now  # record open time as request timestamp
            return Response(500, error=e)
