"""
Tests for the Holdsport object.

Copyright (C) 2026 "Daniel Mizsak" <daniel@mizsak.com>
"""

import httpx2
import pytest

from pyholdsport.holdsport import Holdsport


def test_set_auth_credentials__input_arguments() -> None:
    with Holdsport("argument_username", "argument_password") as holdsport:
        assert holdsport.auth == ("argument_username", "argument_password")


def test_set_auth_credentials__input_arguments_override_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOLDSPORT_USERNAME", "environment_username")
    monkeypatch.setenv("HOLDSPORT_PASSWORD", "environment_password")
    with Holdsport("argument_username", "argument_password") as holdsport:
        assert holdsport.auth == ("argument_username", "argument_password")


def test_set_auth_credentials__input_argument_username_environment_variable_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HOLDSPORT_PASSWORD", "environment_password")
    with Holdsport(holdsport_username="argument_username") as holdsport:
        assert holdsport.auth == ("argument_username", "environment_password")


def test_set_auth_credentials__environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOLDSPORT_USERNAME", "environment_username")
    monkeypatch.setenv("HOLDSPORT_PASSWORD", "environment_password")
    with Holdsport() as holdsport:
        assert holdsport.auth == ("environment_username", "environment_password")


def test_set_auth_credentials__missing_username(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HOLDSPORT_USERNAME", raising=False)
    monkeypatch.setenv("HOLDSPORT_PASSWORD", "environment_password")
    with pytest.raises(
        ValueError,
        match=r"Holdsport username must be provided either as argument or as environment variable HOLDSPORT_USERNAME.",
    ):
        Holdsport()


def test_set_auth_credentials__missing_password(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOLDSPORT_USERNAME", "environment_username")
    monkeypatch.delenv("HOLDSPORT_PASSWORD", raising=False)
    with pytest.raises(
        ValueError,
        match=r"Holdsport password must be provided either as argument or as environment variable HOLDSPORT_PASSWORD.",
    ):
        Holdsport()


def test_holdsport__sets_timeout() -> None:
    with Holdsport("username", "password", timeout=60.0) as holdsport:
        assert holdsport.timeout == 60.0


def test_holdsport__default_client_created_with_timeout() -> None:
    holdsport = Holdsport("username", "password", timeout=60.0)
    assert holdsport._client.timeout == httpx2.Timeout(60.0)
    assert not holdsport._client.is_closed
    holdsport.close()
    assert holdsport._client.is_closed


def test_holdsport__custom_client_used() -> None:
    with httpx2.Client(timeout=10.0) as client:
        holdsport = Holdsport("username", "password", timeout=60.0, client=client)
        assert holdsport._client is client
        assert client.timeout == httpx2.Timeout(10.0)
        holdsport.close()
        assert not client.is_closed
    assert client.is_closed


def test_holdsport__context_manager_closes_client() -> None:
    with Holdsport("username", "password") as holdsport:
        assert not holdsport._client.is_closed
    assert holdsport._client.is_closed


def test_holdsport__context_manager_closes_client_on_exception() -> None:
    holdsport = Holdsport("username", "password")
    msg = "context body failed"
    with pytest.raises(ValueError, match="context body failed"), holdsport:
        raise ValueError(msg)
    assert holdsport._client.is_closed


def test_holdsport__shared_client_remains_usable() -> None:
    requests: list[httpx2.Request] = []

    def handle_request(request: httpx2.Request) -> httpx2.Response:
        requests.append(request)
        return httpx2.Response(200, json=[])

    with httpx2.Client(transport=httpx2.MockTransport(handle_request)) as client:
        with Holdsport("username", "password", client=client) as first:
            assert first.get_teams() == []
            assert first.get_members(123) == []
        assert not client.is_closed

        with Holdsport("username", "password", client=client) as second:
            assert second.get_teams() == []
            first.close()
            assert second.get_members(123) == []

        assert [request.url.path for request in requests] == [
            "/v1/teams",
            "/v1/teams/123/members",
            "/v1/teams",
            "/v1/teams/123/members",
        ]
        assert all(request.headers["Accept"] == "application/json" for request in requests)
        assert all(request.headers["Authorization"] == "Basic dXNlcm5hbWU6cGFzc3dvcmQ=" for request in requests)
    assert client.is_closed
