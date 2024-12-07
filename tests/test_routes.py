from app import create_app
from app.routes import routes
import pytest

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.register_blueprint(routes)  # Ensure the routes are registered
    with app.test_client() as client:
        yield client

def test_fetch_pdf_real_url(client):
    response = client.post('/fetch', data={'url': 'https://www.normanok.gov/sites/default/files/documents/2024-11/2024-11-01_daily_incident_summary.pdf'})
    print(response.data.decode())  # Decode the response content for inspection
    assert response.status_code == 200
    assert b"Clustering Visualization" in response.data
