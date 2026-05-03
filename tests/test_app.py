import pytest

from app import create_app, db
from app.models import User


@pytest.fixture()
def app():
    test_app = create_app()

    test_app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        }
    )

    with test_app.app_context():
        db.drop_all()
        db.create_all()

    yield test_app

    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Security Study Tracker" in response.data


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_register_user(client, app):
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "StrongPassword123!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Login" in response.data

    with app.app_context():
        user = User.query.filter_by(username="testuser").first()

        assert user is not None
        assert user.password_hash != "StrongPassword123!"
        assert user.check_password("StrongPassword123!")


def test_login_user(client):
    client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "StrongPassword123!",
        },
        follow_redirects=True,
    )

    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "StrongPassword123!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Dashboard" in response.data
    assert b"This is a protected page." in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data


def test_logout_user(client):
    client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "StrongPassword123!",
        },
        follow_redirects=True,
    )

    client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "StrongPassword123!",
        },
        follow_redirects=True,
    )

    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"You are not logged in." in response.data
