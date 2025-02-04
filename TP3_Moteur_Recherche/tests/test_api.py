from fastapi.testclient import TestClient
from api import app

# Create a test client for the FastAPI application
client = TestClient(app)

def test_home():
    """
    Test the root endpoint ("/") to ensure it returns a successful response.

    - Expects a 200 status code.
    - Verifies that the response JSON contains the expected welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API de moteur de recherche avec FastAPI"}

def test_search_endpoint():
    """
    Test the "/search" endpoint to ensure it processes search queries correctly.

    - Sends a POST request with a sample search query.
    - Expects a 200 status code.
    - Ensures that the response JSON contains a "results" field.
    """
    response = client.post(
        "/search",
        json={"query": "Chocolate", "search_type": "any", "top_k": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
