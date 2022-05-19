import pytest
from python.user import User
import unittest.mock as um
from unittest import mock


@pytest.fixture
def user(mocker):
    mock_open = mock.mock_open(read_data=b"$2b$12$hEqvUfXW4VXOEENCESztIu")
    with mock.patch("builtins.open", mock_open):
        return User("username", "pass")


def test_init_error():
    """Check init errors in the application"""

    with pytest.raises(ValueError):
        mock_open = mock.mock_open(read_data=b"$2b$12$hEqvUfXW4VXOEENCESztIu")
        with mock.patch("builtins.open", mock_open):
            return User(123, "pass")


def test_init(user):
    """
    check that the init works as expected for attributes
    """
    # make sure the password is different
    assert user.password == "pass"
    assert type(user.encoded_password) == bytes

    mock_open = mock.mock_open(read_data=b"$2b$12$hEqvUfXW4VXOEENCESztIu")
    with mock.patch("builtins.open", mock_open):
        User("name", b"$2b$12$hEqvUfXW4VXOEENCESztIu")


def test_check_password_error(user):
    """make sure the password dycrpter throws the right errors"""
    with pytest.raises(ValueError):

        mock_open = mock.mock_open(read_data=b"$2b$12$hEqvUfXW4VXOEENCESztIu")
        with mock.patch("builtins.open", mock_open):
            user.check_password("name", 111)


def test_check_password(user, mocker):
    """make sure the password can be decrypted"""

    with pytest.raises(ValueError):
        user.check_password("name", 123)

    mock_open = mock.mock_open(read_data=b"$2b$12$hEqvUfXW4VXOEENCESztIu")
    with mock.patch("builtins.open", mock_open):

        assert user.check_password("username", "pass")
        assert not user.check_password("name", "pass")


def test_get_account(user):
    """check the user account return data"""

    assert type(user.get_account()) == dict
