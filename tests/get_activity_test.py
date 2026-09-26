"""
Tests for the get_activity method.

Copyright (C) 2026 "Daniel Mizsak" <daniel@mizsak.com>
"""

import httpx2
import pytest
from pydantic import ValidationError

from pyholdsport import Holdsport, HoldsportActivitiesUser, HoldsportActivity, HoldsportActivityUserStatus
from tests.http_mock import HTTPMock


@pytest.mark.parametrize("status_code", [401, 403, 500])
def test_get_activity__http_error(
    http_mock: HTTPMock,
    team_id: int,
    activity_id: int,
    holdsport: Holdsport,
    status_code: int,
) -> None:
    http_mock.expect(
        "GET",
        f"{holdsport.api_base_url}/teams/{team_id}/activities/{activity_id}",
        response=httpx2.Response(status_code=status_code),
    )

    with pytest.raises(httpx2.HTTPStatusError) as exception_info:
        holdsport.get_activity(team_id=team_id, activity_id=activity_id)

    assert exception_info.value.response.status_code == status_code


def test_get_activity__malformed_response(
    http_mock: HTTPMock,
    team_id: int,
    activity_id: int,
    holdsport: Holdsport,
) -> None:
    http_mock.expect(
        "GET",
        f"{holdsport.api_base_url}/teams/{team_id}/activities/{activity_id}",
        response=httpx2.Response(
            status_code=200,
            json={
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
        ),
    )

    with pytest.raises(ValidationError) as exception_info:
        holdsport.get_activity(team_id=team_id, activity_id=activity_id)

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


@pytest.mark.parametrize(
    "response",
    [httpx2.Response(200, json={}), httpx2.Response(404), httpx2.Response(404, text="Not found")],
    ids=["empty-object", "404-empty", "404-text"],
)
def test_get_activity__no_activity(
    http_mock: HTTPMock,
    team_id: int,
    activity_id: int,
    holdsport: Holdsport,
    response: httpx2.Response,
) -> None:
    http_mock.expect(
        "GET",
        f"{holdsport.api_base_url}/teams/{team_id}/activities/{activity_id}",
        response=response,
    )

    activity = holdsport.get_activity(team_id=team_id, activity_id=activity_id)
    assert activity is None


def test_get_activity__single_activity(
    http_mock: HTTPMock,
    team_id: int,
    activity_id: int,
    holdsport: Holdsport,
) -> None:
    http_mock.expect(
        "GET",
        f"{holdsport.api_base_url}/teams/{team_id}/activities/{activity_id}",
        response=httpx2.Response(
            status_code=200,
            json={
                "id": 1,
                "name": "name",
                "starttime": "2024-01-01T10:00:00Z",
                "endtime": "2024-01-01T12:00:00Z",
                "comment": "comment",
                "place": "place",
                "pickup_place": "pickup_place",
                "pickup_time": "09:30",
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
        ),
    )
    expected_activity = HoldsportActivity(
        id=1,
        name="name",
        starttime="2024-01-01T10:00:00Z",
        endtime="2024-01-01T12:00:00Z",
        comment="comment",
        place="place",
        pickup_place="pickup_place",
        pickup_time="09:30",
        status=1,
        registration_type=1,
        activities_users=[
            HoldsportActivitiesUser(
                id=1,
                name="name",
                status="status",
                status_code=HoldsportActivityUserStatus.ATTENDING,
                updated_at="updated_at",
                user_id=1,
            ),
        ],
        event_type="event_type",
        event_type_id=1,
    )

    activity = holdsport.get_activity(team_id=team_id, activity_id=activity_id)
    assert activity == expected_activity


def test_get_activity__nested_unknown_attendance_status(
    http_mock: HTTPMock,
    team_id: int,
    activity_id: int,
    holdsport: Holdsport,
) -> None:
    http_mock.expect(
        "GET",
        f"{holdsport.api_base_url}/teams/{team_id}/activities/{activity_id}",
        response=httpx2.Response(
            status_code=200,
            json={
                "id": 1,
                "name": "name",
                "starttime": "2024-01-01T10:00:00Z",
                "endtime": "2024-01-01T12:00:00Z",
                "comment": "comment",
                "place": "place",
                "pickup_place": "pickup_place",
                "pickup_time": "09:30",
                "status": 1,
                "registration_type": 1,
                "activities_users": [
                    {
                        "id": 1,
                        "name": "name",
                        "status": "Unknown",
                        "status_code": 5,
                        "updated_at": "updated_at",
                        "user_id": 1,
                    },
                ],
                "event_type": "event_type",
                "event_type_id": 1,
            },
        ),
    )

    activity = holdsport.get_activity(team_id=team_id, activity_id=activity_id)
    assert activity is not None
    users = activity.activities_users
    assert len(users) == 1
    assert users[0].status_code is HoldsportActivityUserStatus.UNKNOWN
    assert users[0].status == "Unknown"
