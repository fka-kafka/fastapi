from typing import List
import pytest
from fastapi.responses import HTMLResponse
from app.database import get_db
from app import models
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.oauth2 import create_access_token

SQLALCHEMY_TEST_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user = {
        'email': "testuser@email.com",
        'password': "password123"
    }

    res = client.post('/users/', json=user)
    user_data = res.json()
    user_data['password'] = user['password']
    assert res.status_code == 201
    return user_data

@pytest.fixture
def test_user2(client):
    user_data = {"email": "testuser2@gmail.com",
                 "password": "password1234"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }

    return client

# @pytest.fixture
# def test_posts(test_user, session):
#     posts_data = [{
#         'title': "First post",
#         'content': "First Test Post",
#         'creator_id': test_user['id']
#     }, {
#         'title': "Second post",
#         'content': "Second Test Post",
#         'creator_id': test_user['id']
#     }, {
#         'title': "Third post",
#         'content': "Third Test Post",
#         'creator_id': test_user['id']
#     }]

#     def create_post_map(post):
#         return models.Post(**post)

#     post_map = map(create_post_map, posts_data)
#     posts = list(post_map)

#     session.add_all(posts)
#     session.commit()

#     posts = session.query(models.Post).all()
#     return posts

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "creator_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "creator_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "creator_id": test_user['id']
    }, {
        "title": "4th title",
        "content": "4th content",
        "creator_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", creator_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", creator_id=test_user['id']), models.Post(title="3rd title", content="3rd content", creator_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts