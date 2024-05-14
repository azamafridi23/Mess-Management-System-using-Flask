def test_student_check_mess_bill_success(client):
    # Simulate student login (set session variable)
    with client.session_transaction() as session:
        session['User_Type'] = 'Student'
        session['user_id'] = 2

    # Send a GET request to view the bill
    response = client.get('/student_check_messbill')

    assert response.status_code == 200
    assert b'student@gmail.com' in response.data 



