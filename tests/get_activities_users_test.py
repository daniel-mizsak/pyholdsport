"""
Tests for the get_activities_users method.

Copyright (C) 2026 "Daniel Mizsak" <daniel@mizsak.com>
"""

import httpx2
import pytest
from pydantic import ValidationError

from pyholdsport import Holdsport, HoldsportActivitiesUser, HoldsportActivityUserStatus
from tests.http_mock import HTTPMock


def test_get_activities_users__invalid_authentication(
    http_mock: HTTPMock,
    activity_id: int,
    holdsport: Holdsport,
) -> None:
    http_mock.expect(
        "GET",
        f"{holdsport.api_base_url}/activities/{activity_id}/activities_users",
        response=httpx2.Response(status_code=401),
    )

    with pytest.raises(httpx2.HTTPStatusError):
        holdsport.get_activities_users(activity_id=activity_id)


def test_get_activities_users__malformed_response(
    http_mock: HTTPMock,
    activity_id: int,
    holdsport: Holdsport,
) -> None:
    http_mock.expect(
        "GET",
        f"{holdsport.api_base_url}/activities/{activity_id}/activities_users",
        response=httpx2.Response(
            status_code=200,
            json=[
                {
                    "id": "string",
                    "name": None,
                    "status": 1,
                    "status_code": "string",
                    "updated_at": 1,
                    "user_id": "string",
                },
            ],
        ),
    )

    with pytest.raises(ValidationError) as exception_info:
        holdsport.get_activities_users(activity_id=activity_id)

    errors = exception_info.value.errors()
    assert len(errors) == 6

    error_details = {(error["loc"][0], error["type"], error["msg"]) for error in errors}
    assert error_details == {
        ("id", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
        ("name", "string_type", "Input should be a valid string"),
        ("status", "string_type", "Input should be a valid string"),
        ("status_code", "enum", "Input should be 1, 2, 3, 4 or 5"),
        ("updated_at", "string_type", "Input should be a valid string"),
        ("user_id", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
    }


def test_get_activities_users(
    http_mock: HTTPMock,
    activity_id: int,
    holdsport: Holdsport,
) -> None:
    http_mock.expect(
        "GET",
        f"{holdsport.api_base_url}/activities/{activity_id}/activities_users",
        response=httpx2.Response(
            status_code=200,
            json=[
                {
                    "id": 1,
                    "name": "name",
                    "status": "status",
                    "status_code": 1,
                    "updated_at": "updated_at",
                    "user_id": 1,
                },
                {
                    "id": 2,
                    "name": "name",
                    "status": "status",
                    "status_code": 2,
                    "updated_at": "updated_at",
                    "user_id": 2,
                },
            ],
        ),
    )
    expected_activities_users = [
        HoldsportActivitiesUser(
            id=1,
            name="name",
            status="status",
            status_code=HoldsportActivityUserStatus.ATTENDING,
            updated_at="updated_at",
            user_id=1,
        ),
        HoldsportActivitiesUser(
            id=2,
            name="name",
            status="status",
            status_code=HoldsportActivityUserStatus.NOT_ATTENDING,
            updated_at="updated_at",
            user_id=2,
        ),
    ]

    activities_users = holdsport.get_activities_users(activity_id=activity_id)
    assert activities_users == expected_activities_users


@pytest.mark.parametrize(
    ("status_code", "status", "expected_status"),
    [
        (1, "Attending", HoldsportActivityUserStatus.ATTENDING),
        (2, "Not attending", HoldsportActivityUserStatus.NOT_ATTENDING),
        (3, "Available", HoldsportActivityUserStatus.AVAILABLE),
        (4, "Selected", HoldsportActivityUserStatus.SELECTED),
        (5, "Unknown", HoldsportActivityUserStatus.UNKNOWN),
    ],
)
def test_get_activities_users__supported_attendance_statuses(
    http_mock: HTTPMock,
    activity_id: int,
    holdsport: Holdsport,
    status_code: int,
    status: str,
    expected_status: HoldsportActivityUserStatus,
) -> None:
    http_mock.expect(
        "GET",
        f"{holdsport.api_base_url}/activities/{activity_id}/activities_users",
        response=httpx2.Response(
            status_code=200,
            json=[
                {
                    "id": 1,
                    "name": "name",
                    "status": status,
                    "status_code": status_code,
                    "updated_at": "updated_at",
                    "user_id": 1,
                },
                {
                    "id": 2,
                    "name": "name",
                    "status": "status",
                    "status_code": 2,
                    "updated_at": "updated_at",
                    "user_id": 2,
                },
            ],
        ),
    )

    users = holdsport.get_activities_users(activity_id=activity_id)
    assert len(users) == 2
    assert users[0].status_code is expected_status
    assert users[0].status == status
    assert users[0].model_dump(mode="json")["status_code"] == status_code
