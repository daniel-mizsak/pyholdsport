"""
Tests for the get_activities method.

@author "Daniel Mizsak" <info@pythonvilag.hu>
"""

import httpx
import pytest
from pydantic import ValidationError
from respx import MockRouter

from pyholdsport import Holdsport, HoldsportActivitiesUser, HoldsportActivity


def test_get_activities__invalid_authentication(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/activities").mock(
        return_value=httpx.Response(status_code=401),
    )

    with pytest.raises(httpx.HTTPStatusError):
        holdsport.get_activities(team_id=team_id)


def test_get_activities__malformed_response(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/activities").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[
                {
                    "id": "string",
                    "name": 1,
                    "starttime": False,
                    "endtime": None,
                    "comment": 1,
                    "place": True,
                    "pickup_place": False,
                    "pickup_time": None,
                    "status": "string",
                    "registration_type": "string",
                    "activities_users": "activities_users",
                    "event_type": None,
                    "event_type_id": "string",
                },
            ],
        ),
    )

    with pytest.raises(ValidationError) as exception_info:
        holdsport.get_activities(team_id=team_id)

    errors = exception_info.value.errors()
    assert len(errors) == 13

    error_details = {(error["loc"][0], error["type"], error["msg"]) for error in errors}
    assert error_details == {
        ("id", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
        ("name", "string_type", "Input should be a valid string"),
        ("starttime", "string_type", "Input should be a valid string"),
        ("endtime", "string_type", "Input should be a valid string"),
        ("comment", "string_type", "Input should be a valid string"),
        ("place", "string_type", "Input should be a valid string"),
        ("pickup_place", "string_type", "Input should be a valid string"),
        ("pickup_time", "string_type", "Input should be a valid string"),
        ("status", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
        ("registration_type", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
        ("activities_users", "list_type", "Input should be a valid list"),
        ("event_type", "string_type", "Input should be a valid string"),
        ("event_type_id", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
    }


def test_get_activities__no_activities(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/activities").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[],
        ),
    )

    activities = holdsport.get_activities(team_id=team_id)
    assert activities == []


def test_get_activities__single_activity(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/activities").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[
                {
                    "id": 1,
                    "name": "name",
                    "starttime": "starttime",
                    "endtime": "endtime",
                    "comment": "comment",
                    "place": "place",
                    "pickup_place": "pickup_place",
                    "pickup_time": "pickup_time",
                    "status": 1,
                    "registration_type": 1,
                    "activities_users": [
                        {
                            "id": 1,
                            "name": "name",
                            "status": "status",
                            "status_code": 1,
                            "updated_at": "updated_at",
                            "user_id": 1,
                        },
                    ],
                    "event_type": "event_type",
                    "event_type_id": 1,
                },
            ],
        ),
    )
    expected_activity = HoldsportActivity(
        id=1,
        name="name",
        starttime="starttime",
        endtime="endtime",
        comment="comment",
        place="place",
        pickup_place="pickup_place",
        pickup_time="pickup_time",
        status=1,
        registration_type=1,
        activities_users=[
            HoldsportActivitiesUser(
                id=1,
                name="name",
                status="status",
                status_code=1,
                updated_at="updated_at",
                user_id=1,
            ),
        ],
        event_type="event_type",
        event_type_id=1,
    )

    activities = holdsport.get_activities(team_id=team_id)
    assert activities == [expected_activity]


def test_get_activities__query_parameters(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    route = respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/activities").mock(
        return_value=httpx.Response(status_code=200, json=[]),
    )

    holdsport.get_activities(team_id=team_id, page=3, per_page=120, date="2026-01-01")
    request = route.calls.last.request
    assert request.url.params["page"] == "3"
    assert request.url.params["per_page"] == "100"
    assert request.url.params["date"] == "2026-01-01"
