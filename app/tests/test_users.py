from fastapi.testclient import TestClient
from app.api import app
from app.models import User
from app.utils import get_hashed_password  # Certifica-te de importar a função de hash corretamente
from app.database import SessionLocal

client = TestClient(app)

def setup_test_user():
    """Adiciona um usuário de teste no banco de dados antes dos testes."""
    db = SessionLocal()
    db.query(User).delete()  # Limpa os usuários antes do teste
    test_user = User(email="test@gmail.com", password=get_hashed_password("Hello1234"))
    db.add(test_user)
    db.commit()
    db.close()

def test_signup():
    response = client.post(
        "/signup",
        json={'email': "test@email.com", "password": "testpassword"}
    )
    
    assert response.status_code == 200, response.data
    assert response.json()['email'] == "test@email.com"

def test_login():
    setup_test_user() 

    response = client.post(
        "/login",
        json={"email": "test@gmail.com", "password": "Hello1234"}
    )

    assert response.status_code == 200, response.data
    json_response = response.json()
    assert "access_token" in json_response
    assert "refresh_token" in json_response
