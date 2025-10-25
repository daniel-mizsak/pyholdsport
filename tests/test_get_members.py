"""
Tests for the get_members method.

@author "Daniel Mizsak" <info@pythonvilag.hu>
"""

import httpx
import pytest
from pydantic import ValidationError
from respx import MockRouter

from pyholdsport import Holdsport, HoldsportAddress, HoldsportMember, HoldsportRole


def test_get_members__invalid_authentication(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/members").mock(return_value=httpx.Response(401))

    with pytest.raises(httpx.HTTPStatusError):
        holdsport.get_members(team_id=team_id)


def test_get_members__malformed_response(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/members").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[
                {
                    "id": "id",
                    "firstname": False,
                    "lastname": 1,
                    "role": -1,
                    "member_number": 1,
                    "birthday": None,
                    "addresses": "addresses",
                    "profile_picture_path": 1,
                },
            ],
        ),
    )

    with pytest.raises(ValidationError) as exception_info:
        holdsport.get_members(team_id=team_id)

    errors = exception_info.value.errors()
    assert len(errors) == 9

    error_details = {(error["loc"][0], error["type"], error["msg"]) for error in errors}
    assert error_details == {
        ("id", "int_parsing", "Input should be a valid integer, unable to parse string as an integer"),
        ("firstname", "string_type", "Input should be a valid string"),
        ("lastname", "string_type", "Input should be a valid string"),
        ("role", "enum", "Input should be 1, 2, 3, 4 or 5"),
        ("member_number", "string_type", "Input should be a valid string"),
        ("birthday", "string_type", "Input should be a valid string"),
        ("birthday", "bool_type", "Input should be a valid boolean"),
        ("addresses", "list_type", "Input should be a valid list"),
        ("profile_picture_path", "string_type", "Input should be a valid string"),
    }


def test_get_members__no_members(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/members").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[],
        ),
    )

    members = holdsport.get_members(team_id=team_id)
    assert members == []


def test_get_members__insufficient_permissions(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/members").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[
                {
                    "id": 1,
                    "firstname": "firstname",
                    "lastname": "lastname",
                    "role": 1,
                    "member_number": "12345",
                    "birthday": False,
                    "addresses": [
                        {
                            "street": "",
                            "city": "",
                            "postcode": "",
                            "telephone": "",
                            "mobile": "",
                            "email": False,
                            "email_ex": False,
                        },
                    ],
                    "profile_picture_path": "profile_picture_path.jpg",
                },
            ],
        ),
    )
    expected_member = HoldsportMember(
        id=1,
        firstname="firstname",
        lastname="lastname",
        role=HoldsportRole.PLAYER,
        member_number="12345",
        birthday=False,
        addresses=[
            HoldsportAddress(street="", city="", postcode="", telephone="", mobile="", email=False, email_ex=False),
        ],
        profile_picture_path="profile_picture_path.jpg",
    )

    members = holdsport.get_members(team_id=team_id)
    assert members == [expected_member]


def test_get_members__sufficient_permissions(respx_mock: MockRouter, team_id: int, holdsport: Holdsport) -> None:
    respx_mock.get(f"{holdsport.api_base_url}/teams/{team_id}/members").mock(
        return_value=httpx.Response(
            status_code=200,
            json=[
                {
                    "id": 1,
                    "firstname": "firstname",
                    "lastname": "lastname",
                    "role": 2,
                    "member_number": "12345",
                    "birthday": "2000-01-01",
                    "addresses": [
                        {
                            "street": "street",
                            "city": "city",
                            "postcode": "postcode",
                            "telephone": "telephone",
                            "mobile": "mobile",
                            "email": "email",
                            "email_ex": None,
                        },
                    ],
                    "profile_picture_path": "profile_picture_path.jpg",
                },
            ],
        ),
    )
    expected_member = HoldsportMember(
        id=1,
        firstname="firstname",
        lastname="lastname",
        role=HoldsportRole.COACH,
        member_number="12345",
        birthday="2000-01-01",
        addresses=[
            HoldsportAddress(
                street="street",
                city="city",
                postcode="postcode",
                telephone="telephone",
                mobile="mobile",
                email="email",
                email_ex=None,
            ),
        ],
        profile_picture_path="profile_picture_path.jpg",
    )

    members = holdsport.get_members(team_id=team_id)
    assert members == [expected_member]
