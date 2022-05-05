import pytest
from python.user import User


@pytest.fixture
def user():
    return User("username", "pass")


def test_init_error():
    """Check init errors in the application"""
    with pytest.raises(ValueError):
        User(123, "pass")
    with pytest.raises(ValueError):
        User("name", 123)


def test_init(user):
    """
    check that the init works as expected for attributes
    """
    # make sure the password is different
    assert user.password != "pass"


def test_check_password_error(user):
    """make sure the password dycrpter throws the right errors"""
    with pytest.raises(ValueError):
        user.check_password("name", 111)


def test_check_password(user):
    """make sure the password can be decrypted"""
    assert user.check_password("username", "pass")
