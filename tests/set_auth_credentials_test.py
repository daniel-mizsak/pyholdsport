"""
Tests for setting authentication credentials.

@author "Daniel Mizsak" <info@pythonvilag.hu>
"""

import pytest

from pyholdsport.holdsport import Holdsport


def test_set_auth_credentials__input_arguments() -> None:
    holdsport = Holdsport("argument_username", "argument_password")
    assert holdsport.auth == ("argument_username", "argument_password")


def test_set_auth_credentials__input_arguments_override_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOLDSPORT_USERNAME", "environment_username")
    monkeypatch.setenv("HOLDSPORT_PASSWORD", "environment_password")
    holdsport = Holdsport("argument_username", "argument_password")
    assert holdsport.auth == ("argument_username", "argument_password")


def test_set_auth_credentials__input_argument_username_environment_variable_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HOLDSPORT_PASSWORD", "environment_password")
    holdsport = Holdsport(holdsport_username="argument_username")
    assert holdsport.auth == ("argument_username", "environment_password")


def test_set_auth_credentials__environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOLDSPORT_USERNAME", "environment_username")
    monkeypatch.setenv("HOLDSPORT_PASSWORD", "environment_password")
    holdsport = Holdsport()
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
