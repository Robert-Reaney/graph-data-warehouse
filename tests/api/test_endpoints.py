import requests as r

def test_health():
    response = r.get('http://localhost:5005/health_check')
    assert response.status_code == 200

# r.get('http://localhost:5005/search/company/152516').json()
