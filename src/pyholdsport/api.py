"""
Holdsport API client.

Official API documentation:
  - https://github.com/Holdsport/holdsport-api

@author "Daniel Mizsak" <info@pythonvilag.hu>
"""

import os

import httpx

from pyholdsport.models import HoldsportActivitiesUser, HoldsportActivity, HoldsportMember, HoldsportTeam


class Holdsport:
    """Class for interacting with Holdsport."""

    def __init__(self, holdsport_username: str | None = None, holdsport_password: str | None = None) -> None:
        """Initialization of the Holdsport object.

        Args:
            holdsport_username (str | None): The Holdsport login username. If not specified environment variable
                HOLDSPORT_USERNAME will be used. If neither are set, an exception will be raised.
            holdsport_password (str | None): The Holdsport login password. If not specified environment variable
                HOLDSPORT_PASSWORD will be used. If neither are set, an exception will be raised.
        """
        self.api_base_url = "https://api.holdsport.dk/v1"
        self.auth = self._set_auth_credentials(holdsport_username, holdsport_password)
        self.headers = {"Accept": "application/json"}

    def _set_auth_credentials(self, holdsport_username: str | None, holdsport_password: str | None) -> tuple[str, str]:
        holdsport_username = holdsport_username or os.getenv("HOLDSPORT_USERNAME")
        if not holdsport_username:
            msg = (
                "Holdsport username must be provided either as argument or as environment variable HOLDSPORT_USERNAME."
            )
            raise ValueError(msg)
        holdsport_password = holdsport_password or os.getenv("HOLDSPORT_PASSWORD")
        if not holdsport_password:
            msg = (
                "Holdsport password must be provided either as argument or as environment variable HOLDSPORT_PASSWORD."
            )
            raise ValueError(msg)
        return (holdsport_username, holdsport_password)

    def get_teams(self) -> list[HoldsportTeam]:
        """Return a list of HoldsportTeam objects the user is member of.

        Returns:
            list[HoldsportTeam]: List of teams the user is member of.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        url = f"{self.api_base_url}/teams"
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            response_dict = response.json()
        return [HoldsportTeam.model_validate(response_entry) for response_entry in response_dict]

    def get_members(self, team_id: int) -> list[HoldsportMember]:
        """Return a list of HoldsportMember objects for the requested team.

        Args:
            team_id (int): The id of the team.

        Returns:
            list[HoldsportMember]: List of members in the requested team.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        url = f"{self.api_base_url}/teams/{team_id}/members"
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            response_dict = response.json()
        return [HoldsportMember.model_validate(response_entry) for response_entry in response_dict]

    def get_member(self, team_id: int, member_id: int) -> HoldsportMember | None:
        """Return a HoldsportMember object for the requested team and member id.

        Args:
            team_id (int): The id of the team.
            member_id (int): The id of the member.

        Returns:
            HoldsportMember | None: The requested member, or None if the member is not found.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        url = f"{self.api_base_url}/teams/{team_id}/members/{member_id}"
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            response_dict = response.json()
        if not response_dict:
            return None
        return HoldsportMember.model_validate(response_dict)

    def get_activities(
        self,
        team_id: int,
        date: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> list[HoldsportActivity]:
        """Return a list of HoldsportActivity objects for the requested team.

        Args:
            team_id (int): The id of the team.
            date (str | None): The starting date to query activities from, in YYYY-MM-DD format.
                If not defined today is used.
            page (int, optional): The page number to query. Defaults to 1. API default is 1.
            per_page (int, optional): The number of activities to query. Defaults to 20.
                API default is 20, maximum is 100.

        Returns:
            list[HoldsportActivity]: List of activities in the requested team.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        url = f"{self.api_base_url}/teams/{team_id}/activities"
        params: dict[str, int | str] = {"page": page, "per_page": min(per_page, 100)}
        if date:
            params["date"] = date
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers, auth=self.auth, params=params)
            response.raise_for_status()
            response_dict = response.json()
        return [HoldsportActivity.model_validate(response_entry) for response_entry in response_dict]

    def get_activity(self, team_id: int, activity_id: int) -> HoldsportActivity | None:
        """Return a HoldsportActivity object for the requested team and activity id.

        Args:
            team_id (int): The id of the team.
            activity_id (int): The id of the activity.

        Returns:
            HoldsportActivity | None: The requested activity, or None if the activity is not found.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        url = f"{self.api_base_url}/teams/{team_id}/activities/{activity_id}"
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            response_dict = response.json()
        if not response_dict:
            return None
        return HoldsportActivity.model_validate(response_dict)

    def get_activities_users(self, activity_id: int) -> list[HoldsportActivitiesUser]:
        """Return a list of HoldsportActivitiesUser objects for the requested activity.

        Args:
            activity_id (int): The id of the activity.

        Returns:
            list[HoldsportActivitiesUser]: List of users in the requested activity.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        url = f"{self.api_base_url}/activities/{activity_id}/activities_users"
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            response_dict = response.json()
        return [HoldsportActivitiesUser.model_validate(response_entry) for response_entry in response_dict]
