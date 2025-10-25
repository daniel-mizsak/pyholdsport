"""
Models for Holdsport API responses.

Should be based on Holdsport OpenAPI, but the document was not up-to-date:
  - https://github.com/Holdsport/holdsport-api/blob/master/openapi.yml

@author "Daniel Mizsak" <info@pythonvilag.hu>
"""

from enum import IntEnum

from pydantic import BaseModel, Field


class HoldsportTeam(BaseModel):
    """Data model for team in Holdsport."""

    id: int
    name: str
    primary_color: str
    secondary_color: str
    role: "HoldsportRole"


class HoldsportMember(BaseModel):
    """Data model for member in Holdsport."""

    id: int
    firstname: str
    lastname: str
    role: "HoldsportRole"
    member_number: str
    birthday: str | bool = Field(description="Return value is False for insufficient permissions")
    addresses: list["HoldsportAddress"]
    profile_picture_path: str
    # club_fields: list[HoldsportClubField]  # Not added as I do not know what this is for.  # noqa: ERA001


class HoldsportActivity(BaseModel):
    """Data model for activity in Holdsport."""

    id: int
    # club: str  # noqa: ERA001
    # department: str  # noqa: ERA001
    name: str
    starttime: str
    endtime: str
    comment: str
    place: str
    pickup_place: str
    pickup_time: str
    status: int
    registration_type: int
    # actions: list  # noqa: ERA001
    # action_path: str  # noqa: ERA001
    # action_method: str  # noqa: ERA001
    activities_users: list["HoldsportActivitiesUser"]
    # ride: bool  # noqa: ERA001
    # ride_comment: str  # noqa: ERA001
    # rides: list  # noqa: ERA001
    # show_ride_button: bool  # noqa: ERA001
    event_type: str
    event_type_id: int


class HoldsportActivitiesUser(BaseModel):
    """Data model for activity user in Holdsport."""

    id: int
    name: str
    status: str  # TODO: Enum?
    status_code: int
    updated_at: str
    user_id: int


class HoldsportRole(IntEnum):
    """Holdsport member role enumeration."""

    PLAYER = 1
    COACH = 2
    ASSISTANT_COACH = 3
    INJURED = 4
    INACTIVE = 5


class HoldsportAddress(BaseModel):
    """Data model for address in Holdsport."""

    street: str = Field(description="Return value is empty for insufficient permissions")
    city: str = Field(description="Return value is empty for insufficient permissions")
    postcode: str = Field(description="Return value is empty for insufficient permissions")
    telephone: str = Field(description="Return value is empty for insufficient permissions")
    mobile: str = Field(description="Return value is empty for insufficient permissions")
    email: str | None | bool = Field(description="Return value is False for insufficient permissions")
    email_ex: str | None | bool = Field(description="Return value is False for insufficient permissions")
    # parents_name: str | None  # Not added as I do not have access to example response.  # noqa: ERA001


class HoldsportNote(BaseModel):
    """Data model for note in Holdsport."""

    # attachment_path: str  # noqa: ERA001
    body: str
    create_at: str
    created_by: str
    title: str
