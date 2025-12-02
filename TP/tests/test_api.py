import pytest
from triangulator.api import create_app

# Tests unitaires pour l'API de triangulation
def test_api_success(mocker):
    app = create_app()
    client = app.test_client()

    # faux binaire pour simuler un pointset
    fake_pointset = b"\x00\x00\x00\x01" + b"\x00"*8

    fake_response = mocker.Mock()
    fake_response.status_code = 200
    fake_response.content = fake_pointset

    mocker.patch("triangulator.api.requests.get", return_value=fake_response)

    response = client.get("/triangulate?set_id=1")
    assert response.status_code == 200

def test_missing_set_id():
    app = create_app()
    client = app.test_client()
    response = client.get("/triangulate")
    assert response.status_code == 400 # Verifie que l'absence de set_id retourne 400

def test_invalid_set_id():
    app = create_app()
    client = app.test_client()
    response = client.get("/triangulate?set_id=abc")
    assert response.status_code == 400 # Verifie que un set_id non entier retourne 400

def test_pointsetmanager_failure(mocker):
    app = create_app()
    client = app.test_client()

    fake_response = mocker.Mock()
    fake_response.status_code = 500

    mocker.patch("triangulator.api.requests.get", return_value=fake_response)

    response = client.get("/triangulate?set_id=1")
    assert response.status_code == 502 # Verifie que une erreur du service externe retourne 502
