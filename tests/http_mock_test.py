"""
Verify that HTTP mocks fail on unexpected or missing requests.

Copyright (C) 2026 "Daniel Mizsak" <daniel@mizsak.com>
"""

import httpx2
import pytest

from tests.http_mock import HTTPMock


@pytest.mark.parametrize(
    ("method", "url"),
    [
        ("POST", "https://example.test/teams?page=1"),
        ("GET", "https://example.test/members?page=1"),
        ("GET", "https://other.test/teams?page=1"),
        ("GET", "https://example.test/teams?page=2"),
    ],
)
def test_http_mock__rejects_mismatched_request(method: str, url: str) -> None:
    mock = HTTPMock()
    mock.expect("GET", "https://example.test/teams?page=1", response=httpx2.Response(200))
    with httpx2.Client(transport=httpx2.MockTransport(mock.handle_request)) as client:
        with pytest.raises(AssertionError, match="Expected"):
            client.request(method, url)
        with pytest.raises(AssertionError, match="Uncalled requests"):
            mock.assert_all_called()


def test_http_mock__rejects_unconfigured_and_extra_requests() -> None:
    mock = HTTPMock()
    with httpx2.Client(transport=httpx2.MockTransport(mock.handle_request)) as client:
        with pytest.raises(AssertionError, match="Unexpected request"):
            client.get("https://example.test/teams")

        mock.expect("GET", "https://example.test/teams", response=httpx2.Response(200))
        assert client.get("https://example.test/teams").status_code == 200
        mock.assert_all_called()

        with pytest.raises(AssertionError, match="Unexpected request"):
            client.get("https://example.test/teams")


def test_http_mock__rejects_unused_expectation() -> None:
    mock = HTTPMock()
    mock.expect("GET", "https://example.test/teams", response=httpx2.Response(200))
    with pytest.raises(AssertionError, match="Uncalled requests"):
        mock.assert_all_called()
