import pytest
from app.schemas.user import User


def test_user_schema():
    user = User(username='Edson', password='pass#')
    assert user.dict() == {
        "username": "Edson",
        "password": "pass#"
    }


def test_user_schema_invalid_schema():
    with pytest.raises(ValueError):
        user = User(username='Edsãon', password='pass#')
