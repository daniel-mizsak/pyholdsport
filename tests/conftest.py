"""
Fixtures used in testing the library.

Copyright (C) 2026 "Daniel Mizsak" <daniel@mizsak.com>
"""

from collections.abc import Iterator

import pytest

from pyholdsport.holdsport import Holdsport


@pytest.fixture(name="holdsport")
def holdsport_fixture() -> Iterator[Holdsport]:
    with Holdsport("username", "password") as holdsport:
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
