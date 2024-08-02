from app.schemas import UserResponse
import pytest
from jose import jwt
from app.config import settings
from app.schemas import Token


def test_create_user(client):
    res = client.post(
        '/users/', json={'email': 'example@email.com', 'password': 'password123'})
    user = UserResponse(**res.json())
    assert user.email == "example@email.com" and res.status_code == 201


def test_login(client, test_user):
    res = client.post(
        '/login', data={'username': test_user['email'], 'password': test_user['password']})
    token = Token(**res.json())
    payload = jwt.decode(token.access_token,
                         settings.secret_key, algorithms=settings.algorithm)
    id = payload.get("user_id")
    assert res.status_code == 200 and token.token_type == "bearer" and id == test_user['id']


@pytest.mark.parametrize('email, password, status_code', [
    ('testuser@gmail.com', 'password123', 403),
    ('testuser@email.com', 'password1234', 403),
    ('testuser@gmail.com', 'password1234', 403),
    (None, 'password123', 422),
    ('testuser@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})

    assert res.status_code == status_code
