import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.services.user import UserService
from app.schemas.user import UserIn
from app.models.user import User as UserModel
from app.schemas.token import Token
from app.services.utils import UtilsService


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def mock_user():
    return UserModel(id=1, email="testuser@example.com", password=UtilsService.get_password_hash("password123"))


@pytest.mark.asyncio
async def test_register_user_success(mock_session):

    mock_session.execute.return_value.scalars.return_value.first.return_value = None
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    user_data = UserIn(email="tanaka@example.com", password="password123", first_name="Test", last_name="User")

    with patch("app.daos.user.UserDao.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = UserModel(id=3, email=user_data.email)
        response = await UserService.register_user(user_data, mock_session)

    assert response.status_code == 201
    assert response.body == b'{"message":"User created successfully"}'

@pytest.mark.asyncio
async def test_register_already_existing_user_success(mock_session):

    mock_session.execute.return_value.scalars.return_value.first.return_value = None
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    user_data = UserIn(email="testAdmin@example.com", password="password123", first_name="Test", last_name="User")

    with patch("app.daos.user.UserDao.create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = UserModel(id=2, email=user_data.email)
        response = await UserService.register_user(user_data, mock_session)

    assert response.status_code == 400
    assert response.body == b'{"message":"User with the given email already exists!!!"}'


@pytest.mark.asyncio
async def test_register_user_existing_email(mock_session, mock_user):
    with patch("app.daos.user.UserDao.get_by_email", new_callable=AsyncMock) as mock_get_by_email:
        mock_get_by_email.return_value = mock_user

        user_data = UserIn(email="testuser@example.com", password="password123", first_name="Test", last_name="User")

        with pytest.raises(HTTPException) as exc_info:
            await UserService.register_user(user_data, mock_session)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User with the given email already exists!!!"


@pytest.mark.asyncio
async def test_authenticate_user_success(mock_session, mock_user):
    with patch("app.daos.user.UserDao.get_by_email", new_callable=AsyncMock) as mock_get_by_email:
        mock_get_by_email.return_value = mock_user

        authenticated_user = await UserService.authenticate_user(mock_session, "testuser@example.com", "password123")

    assert authenticated_user is not False
    assert authenticated_user.email == "testuser@example.com"


@pytest.mark.asyncio
async def test_authenticate_user_invalid_credentials(mock_session):
    with patch("app.daos.user.UserDao.get_by_email", new_callable=AsyncMock) as mock_get_by_email:
        mock_get_by_email.return_value = None  # User not found

        result = await UserService.authenticate_user(mock_session, "wronguser@example.com", "password123")

    assert result is False


@pytest.mark.asyncio
async def test_login_success(mock_session, mock_user):

    with patch("app.services.utils.UtilsService.create_access_token", return_value="fake_token"), \
         patch("app.daos.user.UserDao.get_by_email", new_callable=AsyncMock) as mock_get_by_email:

        mock_get_by_email.return_value = mock_user

        form_data = AsyncMock(username="testuser@example.com", password="password123")
        token: Token = await UserService.login(form_data, mock_session)

    assert token.access_token == "fake_token"
    assert token.token_type == "Bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(mock_session):

    with patch("app.daos.user.UserDao.get_by_email", new_callable=AsyncMock) as mock_get_by_email:
        mock_get_by_email.return_value = None

        form_data = AsyncMock(username="wronguser@example.com", password="password123")

        with pytest.raises(HTTPException) as exc_info:
            await UserService.login(form_data, mock_session)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Incorrect email or password"




