from triangulator.api import create_app


def test_api_success(monkeypatch):
    app = create_app()
    client = app.test_client()

    # Faux binaire pour simuler un pointset valide
    fake_pointset = b"\x00\x00\x00\x01" + b"\x00" * 8

    class FakeResponse:
        status_code = 200
        content = fake_pointset

    # Mock de requests.get
    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "triangulator.api.requests.get",
        fake_get
    )

    response = client.get("/triangulate?set_id=1")
    assert response.status_code == 200


def test_missing_set_id():
    app = create_app()
    client = app.test_client()

    response = client.get("/triangulate")
    assert response.status_code == 400  # absence de set_id


def test_invalid_set_id():
    app = create_app()
    client = app.test_client()

    response = client.get("/triangulate?set_id=abc")
    assert response.status_code == 400  # set_id non entier


def test_pointsetmanager_failure(monkeypatch):
    app = create_app()
    client = app.test_client()

    class FakeResponse:
        status_code = 500
        content = b""

    # Mock simulant une erreur du service externe
    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "triangulator.api.requests.get",
        fake_get
    )

    response = client.get("/triangulate?set_id=1")
    assert response.status_code == 502  # erreur service externe
