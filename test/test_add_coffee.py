from unittest.mock import Mock
from fastapi.testclient import TestClient
from requests.sessions import session

from main import app
from routers.coffee import add_coffee
from schemas import CoffeeInput, User, Coffee

client = TestClient(app)


def test_get_coffee():
    data = {"username": "codewizz", "password": "python555%%"}
    resp_token = client.post("/auth/token", data=data)
    token = resp_token.json().get("access_token")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    r = client.get("/api/coffee", headers=headers)
    assert r.status_code == 200


def test_get_coffee_no_auth():
    r = client.get("/api/coffee")
    assert r.status_code == 401


def test_add_coffee_with_mock_session():
    mock_session = Mock()
    input = CoffeeInput(
        name="Mocha",
        price=59,
        status="a"
    )
    result = add_coffee(coffee=input, db=mock_session)
    
    __import__('pdb').set_trace()
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert isinstance(result, Coffee)
    assert result.name=="Mocha"
    
