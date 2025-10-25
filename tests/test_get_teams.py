"""
Tests for the get_teams method.

@author "Daniel Mizsak" <info@pythonvilag.hu>
"""

import httpx
import pytest
from pydantic import ValidationError
from respx import MockRouter

from pyholdsport import Holdsport, HoldsportRole, HoldsportTeam


def test_get_teams__invalid_authentication(respx_mock: MockRouter, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams").mock(return_value=httpx.Response(status_code=401))

    with pytest.raises(httpx.HTTPStatusError):
        holdsport.get_teams()


def test_get_teams__malformed_response(respx_mock: MockRouter, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[
                {
                    "id": "not-an-integer",
                    "name": False,
                    "primary_color": 2,
                    "role": -1,
                },
            ],
        ),
    )

    with pytest.raises(ValidationError) as exception_info:
        holdsport.get_teams()

    errors = exception_info.value.errors()
    assert len(errors) == 5

    error_details = {(error["loc"][0], error["type"], error["msg"]) for error in errors}
    assert error_details == {
        ("id", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
        ("name", "string_type", "Input should be a valid string"),
        ("primary_color", "string_type", "Input should be a valid string"),
        ("secondary_color", "missing", "Field required"),
        ("role", "enum", "Input should be 1, 2, 3, 4 or 5"),
    }


def test_get_teams__no_teams(respx_mock: MockRouter, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[],
        ),
    )

    teams = holdsport.get_teams()
    assert teams == []


def test_get_teams__single_team(respx_mock: MockRouter, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[
                {
                    "id": 1,
                    "name": "name",
                    "primary_color": "",
                    "secondary_color": "",
                    "role": 1,
                },
            ],
        ),
    )
    expected_team = HoldsportTeam(
        id=1,
        name="name",
        primary_color="",
        secondary_color="",
        role=HoldsportRole.PLAYER,
    )

    teams = holdsport.get_teams()
    assert teams == [expected_team]


def test_get_teams__multiple_teams(respx_mock: MockRouter, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[
                {
                    "id": 1,
                    "name": "A Team",
                    "primary_color": "#111111",
                    "secondary_color": "#222222",
                    "role": 3,
                },
                {
                    "id": 2,
                    "name": "B Team",
                    "primary_color": "#333333",
                    "secondary_color": "#444444",
                    "role": 2,
                },
            ],
        ),
    )
    expected_teams = [
        HoldsportTeam(
            id=1,
            name="A Team",
            primary_color="#111111",
            secondary_color="#222222",
            role=HoldsportRole.ASSISTANT_COACH,
        ),
        HoldsportTeam(
            id=2,
            name="B Team",
            primary_color="#333333",
            secondary_color="#444444",
            role=HoldsportRole.COACH,
        ),
    ]

    teams = holdsport.get_teams()
    assert len(teams) == len(expected_teams)
    for team in teams:
        assert team in expected_teams
