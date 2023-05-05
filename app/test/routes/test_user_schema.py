import pytest
from app.schemas.user import User


def test_user_schema():
    user = User(username='Edson', password='pass#')
    assert user.dict() == {
        "username": "Edson",
        "password": "pass#"
    }
