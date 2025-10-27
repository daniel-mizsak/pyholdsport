"""
Fixtures used in testing the library.

@author "Daniel Mizsak" <info@pythonvilag.hu>
"""

import pytest

from pyholdsport.holdsport import Holdsport


@pytest.fixture(name="holdsport")
def holdsport_fixture() -> Holdsport:
    return Holdsport("username", "password")


@pytest.fixture(name="team_id")
def team_id_fixture() -> int:
    return 123


@pytest.fixture(name="member_id")
def member_id_fixture() -> int:
    return 1234


@pytest.fixture(name="activity_id")
def activity_id_fixture() -> int:
    return 12345
