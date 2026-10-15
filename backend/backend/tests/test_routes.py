from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_import_invalid_file():
    response = client.post('/api/games/import', files={'file':('test.txt','not pgn')})
    assert response.status_code == 400
