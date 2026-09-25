"""
Strict request expectations for HTTPX2 tests.

Used with httpx2.MockTransport as documented at:
https://pydantic.dev/docs/httpx2/advanced/transports/#mock-transports

Copyright (C) 2026 "Daniel Mizsak" <daniel@mizsak.com>
"""

from collections import deque

import httpx2


class HTTPMock:
    def __init__(self) -> None:
        self.requests: list[httpx2.Request] = []
        self._expected: deque[tuple[str, httpx2.URL, httpx2.Response]] = deque()

    def expect(self, method: str, url: str, *, response: httpx2.Response) -> None:
        self._expected.append((method, httpx2.URL(url), response))

    def handle_request(self, request: httpx2.Request) -> httpx2.Response:
        self.requests.append(request)
        assert self._expected, f"Unexpected request: {request.method} {request.url}"
        method, url, response = self._expected[0]
        # Mismatches leave the expectation pending, so teardown also reports it as uncalled.
        assert request.method == method, f"Expected {method}, got {request.method}"
        assert request.url == url, f"Expected {url}, got {request.url}"
        self._expected.popleft()
        return response

    def assert_all_called(self) -> None:
        assert not self._expected, f"Uncalled requests: {[(method, str(url)) for method, url, _ in self._expected]}"
