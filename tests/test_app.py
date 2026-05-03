from app import app


def test_homepage_loads():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Security+ Study Tracker" in response.data


def test_progress_text_exists():
    client = app.test_client()
    response = client.get("/")

    assert b"Progress:" in response.data
