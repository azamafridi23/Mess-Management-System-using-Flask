def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_signin_page(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_signin_page(client):
    response = client.get('/signup')
    assert response.status_code == 200

def test_signin_page(client):
    response = client.get('/aboutus')
    assert response.status_code == 200
