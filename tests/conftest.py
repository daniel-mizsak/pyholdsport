"""
Fixtures used in testing the library.

Copyright (C) 2026 "Daniel Mizsak" <daniel@mizsak.com>
"""

from collections.abc import Iterator

import httpx2
import pytest

from pyholdsport.holdsport import Holdsport
from tests.http_mock import HTTPMock


@pytest.fixture(name="http_mock")
def http_mock_fixture() -> Iterator[HTTPMock]:
    mock = HTTPMock()
    yield mock
    mock.assert_all_called()


@pytest.fixture(name="holdsport")
def holdsport_fixture(http_mock: HTTPMock) -> Iterator[Holdsport]:
    with (
        httpx2.Client(transport=httpx2.MockTransport(http_mock.handle_request)) as client,
        Holdsport("username", "password", client=client) as holdsport,
    ):
        yield holdsport


@pytest.fixture(name="team_id")
def team_id_fixture() -> int:
    return 123


@pytest.fixture(name="member_id")
def member_id_fixture() -> int:
    return 1234


@pytest.fixture(name="activity_id")
def activity_id_fixture() -> int:
    return 12345
