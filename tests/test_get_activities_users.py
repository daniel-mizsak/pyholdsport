"""
Tests for the get_activities_users method.

@author "Daniel Mizsak" <info@pythonvilag.hu>
"""

import httpx
import pytest
from pydantic import ValidationError
from respx import MockRouter

from pyholdsport import Holdsport, HoldsportActivitiesUser


def test_get_activities_users__invalid_authentication(
    respx_mock: MockRouter,
    activity_id: int,
    holdsport: Holdsport,
) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/activities/{activity_id}/activities_users").mock(
        return_value=httpx.Response(status_code=401),
    )

    with pytest.raises(httpx.HTTPStatusError):
        holdsport.get_activities_users(activity_id=activity_id)


def test_get_activities_users__malformed_response(
    respx_mock: MockRouter,
    activity_id: int,
    holdsport: Holdsport,
) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/activities/{activity_id}/activities_users").mock(
        return_value=httpx.Response(
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
        ("status_code", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
        ("updated_at", "string_type", "Input should be a valid string"),
        ("user_id", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
    }


def test_get_activities_users(
    respx_mock: MockRouter,
    activity_id: int,
    holdsport: Holdsport,
) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/activities/{activity_id}/activities_users").mock(
        return_value=httpx.Response(
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
            status_code=1,
            updated_at="updated_at",
            user_id=1,
        ),
        HoldsportActivitiesUser(
            id=2,
            name="name",
            status="status",
            status_code=2,
            updated_at="updated_at",
            user_id=2,
        ),
    ]

    activities_users = holdsport.get_activities_users(activity_id=activity_id)
    assert activities_users == expected_activities_users
