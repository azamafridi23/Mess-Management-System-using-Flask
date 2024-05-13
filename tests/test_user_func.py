'''
In Flask testing, client.session_transaction() is a context manager specifically designed to manipulate the session object within a test.
It allows you to temporarily modify the session for the duration of a code block and ensures the changes are properly stored after the block executes

'''

def test_display_menu_student_logged_in(client):
    # Simulate successful student login (set session variable)
    with client.session_transaction() as session:
        session['User_Type'] = 'Student'

    response = client.get('/display_menu_for_student')

    assert response.status_code == 200
    assert b'cereal' in response.data  # Check for presence of menu item in response

def test_failed_display_menu_student_logged_in(client):
    # Simulate successful student login (set session variable)
    with client.session_transaction() as session:
        session['User_Type'] = ''

    response = client.get('/display_menu_for_student')

    assert response.status_code == 200
    assert b'NOT ALLOWED' in response.data  # Check for presence of menu item in response