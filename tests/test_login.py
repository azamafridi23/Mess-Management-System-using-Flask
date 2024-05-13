def test_successful_login_student(client):
    # Login form data
    data = {'User_Email': 'student@gmail.com', 'User_Password': '1234'}

    response = client.post('/auth', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert 'studentView' in response.request.url

def test_successful_login_supervisor(client):
    # Login form data
    data = {'User_Email': 'sv@gmail.com', 'User_Password': '1234'}

    response = client.post('/auth', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert 'supervisorView' in response.request.url

def test_unsuccessful_login_supervisor(client):
    '''
    Incorrect password
    '''
    # Login form data
    data = {'User_Email': 'sv@gmail.com', 'User_Password': '12345'}

    response = client.post('/auth', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.url.endswith('/auth')
    assert b'Invalid Email or Password Try Again!' in response.data

def test_unsuccessful_login_student(client):
    '''
    Incorrect password
    '''
    data = {'User_Email': 'student@gmail.com', 'User_Password': '12345'}

    response = client.post('/auth', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.url.endswith('/auth')
    assert b'Invalid Email or Password Try Again!' in response.data
