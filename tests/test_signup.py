def test_successful_signup(client):
    # Sign-up form data
    data = {
        'Enter_name_for_signup': 'Test User',
        'Enter_email_for_sigup': 'test@example.com',
        'Enter_password_for_signup': 'valid_password',
        'Roles_SS': 'Student'
    }

    response = client.post('/signup2', data=data, follow_redirects=True)

    assert response.status_code == 200
    #assert b'Account created successfully!' in response.data

def test_signup_existing_email(client, monkeypatch):
    # Sign-up form data with an existing email
    data = {
        'Enter_name_for_signup': 'Test User',
        'Enter_email_for_sigup': 'test@example.com',
        'Enter_password_for_signup': 'valid_password',
        'Roles_SS': 'Student'
    }

    response = client.post('/signup2', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.url.endswith('/signup')
    assert b'Account already exists!' in response.data
