'''
This functionality depends on the current time at which the action is being performed
'''

def test_student_checkin_success_breakfast(client):
    # Simulate student login (set session variable)
    with client.session_transaction() as session:
        session['User_Type'] = 'Student'
        session['user_id'] = 2  # Replace with actual user ID

    # Send a POST request for breakfast check-in (no previous entry)
    data = {'meal_type': 'bf'}
    response = client.post('/student_checkin', data=data)

    assert response.status_code == 200
    assert b'NOT ALLOWED TO MESS OUT AFTER 11' in response.data  # Check for success message

def test_student_checkout_success_breakfast(client):
    # Simulate student login (set session variable)
    with client.session_transaction() as session:
        session['User_Type'] = 'Student'
        session['user_id'] = 2  # Replace with actual user ID

    # Send a POST request for breakfast check-in (no previous entry)
    data = {'meal_type': 'bf'}
    response = client.post('/student_checkout', data=data)

    assert response.status_code == 200
    assert b'NOT ALLOWED TO MESS OUT AFTER 11' in response.data  # Check for success message