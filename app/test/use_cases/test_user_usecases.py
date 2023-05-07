import pytest
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from app.schemas.user import User, TokenData
from app.db.models import User as UserModel
from app.use_cases.user_use_cases import UserUseCases

crypt_context = CryptContext(schemes=['sha256_crypt'])


def test_register_user(db_session):
    user = User(
        username='Diogo',
        password='pass#'
    )

    uc = UserUseCases(db_session)
    uc.register_user(user=user)

    user_on_db = db_session.query(UserModel).first()
    assert user_on_db is not None
    assert user_on_db.username == user.username
    assert crypt_context.verify(user.password, user_on_db.password)

    db_session.delete(user_on_db)
    db_session.commit()


def test_register_user_username_already_exists(db_session):
    user_on_db = UserModel(
        username="Diogo",
        password=crypt_context.hash('pass#')
    )

    db_session.add(user_on_db)
    db_session.commit()

    uc = UserUseCases(db_session)

    user = User(
        username='Diogo',
        password=crypt_context.hash('pass#')
    )

    with pytest.raises(HTTPException):
        uc.register_user(user=user)

    db_session.delete(user_on_db)
    db_session.commit()


def test_token_date():
    expires_at = datetime.now()
    token_data = TokenData(
        access_token='token qualquer',
        expires_at=expires_at
    )

    assert token_data.dict() == {
        'access_token': 'token qualquer',
        'expires_at': expires_at
    }


def test_user_login(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)

    user = User(
        username=user_on_db.username,
        password='pass#'
    )

    token_data = uc.user_login(user=user, expires_in=30)

    assert token_data.expires_at < datetime.utcnow() + timedelta(31)
