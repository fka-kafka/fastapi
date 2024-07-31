from app.config import settings
from jose import jwt
from app.schemas import UserResponse, Token
import pytest

def test_root(client):
    res = client.get('/')
    content_type = res.headers['content-type']
    assert content_type == 'text/html; charset=utf-8' and res.status_code == 200

def test_create_user(client):
    res = client.post('/users/', json={'email': 'example@email.com', 'password': 'password123'})
    user = UserResponse(**res.json())
    assert user.email == "example@email.com" and res.status_code == 201

def test_login(client, test_user):
    res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    token = Token(**res.json())
    payload = jwt.decode(token.access_token, settings.secret_key, algorithms=settings.algorithm)
    id = payload.get("user_id")
    assert res.status_code == 200 and token.token_type == "bearer" and id == test_user['id']
