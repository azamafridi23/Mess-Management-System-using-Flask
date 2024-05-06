from flask import Flask ,render_template,jsonify,request, redirect, url_for, g,session,flash
import time
import os
import hashlib
import sqlite3
from datetime import datetime
app=Flask(__name__)
app.secret_key = 'FullStackProject'
DATABASE = 'users.db'
DATABASE2 = 'reveiws.db'
# azam code
def create_connection_for_menu():
    DATABASE = 'menu.db'
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table_for_menu(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT,
                breakfast TEXT,
                lunch TEXT,
                dinner TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        
# azam code
def create_connection_for_check_mess():
    DATABASE1 = 'ld.db'
    DATABASE2 = 'breakfast.db'
    conn1,conn2 = None,None
    try:
        conn1  = sqlite3.connect(DATABASE1)
        conn2 = sqlite3.connect(DATABASE2)
    except sqlite3.Error as e:
        print(e)
    return conn1,conn2

def create_table_for_check_mess(conn1,conn2):
    try:
        cursor = conn1.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS LD (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_id INTEGER,
                Check_status TEXT,
                Date DATE,
                Time TIME,
                Counter INTEGER,
                FOREIGN KEY (User_id) REFERENCES users(id)
            )
        ''')
        conn1.commit()
        cursor = conn2.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS BREAKFAST (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_id INTEGER,
                Check_status TEXT,
                Date DATE,
                Time TIME,
                Counter INTEGER,
                FOREIGN KEY (User_id) REFERENCES users(id)
            )
        ''')
        conn2.commit()
        return 'ok'
    except sqlite3.Error as e:
        print(e)
        return 'failed'
    

def temp_db_cmnds():
    conn_ld,conn_bf = create_connection_for_check_mess()
    cursor = conn_bf.cursor()
    cursor.execute('''INSERT INTO BREAKFAST (User_id, Check_status, Date,Time,Counter) VALUES (?, ?, ?, ?,?)''', (1,'IN',"2024-05-01","11:18:11",1))
    conn_bf.commit()
    cursor.close()

    cursor = conn_ld.cursor()
    cursor.execute('''INSERT INTO LD (User_id, Check_status, Date,Time,Counter) VALUES (?, ?, ?, ?,?)''', (1,'IN',"2024-05-01","11:18:11",1))
    conn_ld.commit()
    cursor.close()

    conn_ld.close()
    conn_bf.close()


@app.route('/student_checkin',methods=['GET','POST'])
def checkin():
    print(f'came in student_checkin2')
    if request.method == 'GET':
        return render_template("/mess_checkin.html")
    
    # Else its post request
    conn_ld,conn_bf = create_connection_for_check_mess()
    if conn_ld is not None and conn_bf is not None:
        try:
            result = create_table_for_check_mess(conn1=conn_ld,conn2=conn_bf)
            # temp_db_cmnds()
            if result =='fail':
                return 'TABLE LD AND BF CREATION ERROR', 500
            
            data = request.form # change to change.form
            print(f'data = {data}')
            user_id = session.get('user_id')
            meal_type = data['meal_type']
            
            # Get the current date
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            
            current_date_str = current_date.strftime('%Y-%m-%d')
            current_time_str = current_time.strftime('%H:%M:%S')
            if meal_type=='bf':
                cursor = conn_bf.cursor()
                sql_query = "SELECT * FROM BREAKFAST WHERE User_id = ? ORDER BY id DESC LIMIT 1" # select last entry of User_id
                # Execute the query with user_id=1
                cursor.execute(sql_query, (user_id,))
                # Fetch the result
                last_entry = cursor.fetchone()
                # Print or process the last entry
                print(f'le = ',last_entry)
                
                if last_entry is None:
                    print('a')
                    cursor.execute('''INSERT INTO BREAKFAST (User_id, Check_status, Date,Time, Counter) VALUES (?, ?, ?, ?,?)''', (user_id,'IN',current_date_str,current_time_str,1))
                    print('b')
                    conn_bf.commit()
                    print('c')
                else:
                    last_entry_date = datetime.strptime(last_entry[3], "%Y-%m-%d").date()
                    diff = (current_date - last_entry_date).days
                    print(f'diff = {diff}')
                    if current_time.hour > 20:
                        return 'NOT ALLOWED TO MESS IN AFTER 11',200
                    elif last_entry[2]=='IN':
                        return 'ALREADY MESS IN',200
                    else:
                        counter = last_entry[5] + diff
                        cursor.execute('''INSERT INTO BREAKFAST (User_id, Check_status, Date,Time, Counter) VALUES (?, ?, ?, ?,?)''', (user_id,'IN',current_date_str,current_time_str,counter))
                        conn_bf.commit()
                # Don't forget to close the cursor and connection when done
                cursor.close()
                conn_bf.close()
            elif meal_type=='ld':
                cursor = conn_ld.cursor()
                sql_query = "SELECT * FROM LD WHERE User_id = ? ORDER BY id DESC LIMIT 1" # select last entry of User_id
                # Execute the query with user_id=1
                cursor.execute(sql_query, (user_id,))
                # Fetch the result
                last_entry = cursor.fetchone()
                # Print or process the last entry
                print(f'last entry = {last_entry}')
                if last_entry is None:
                    cursor.execute('''INSERT INTO LD (User_id, Check_status, Date,Time, Counter) VALUES (?, ?, ?, ?,?)''', (user_id,'IN',current_date_str,current_time_str,1))
                    conn_ld.commit()
                else:
                    last_entry_date = datetime.strptime(last_entry[3], "%Y-%m-%d").date()
                    diff = (current_date - last_entry_date).days
                    print(f'diff = {diff}')
                    if current_time.hour > 20:
                        return 'NOT ALLOWED TO MESS IN AFTER 11',200
                    elif last_entry[2]=='IN':
                        return 'ALREADY MESS IN',200
                    else:
                        counter = last_entry[5] + diff
                        cursor.execute('''INSERT INTO LD (User_id, Check_status, Date,Time,Counter) VALUES (?, ?, ?, ?,?)''', (user_id,'IN',current_date_str,current_time_str,counter))
                        conn_ld.commit()
                # Don't forget to close the cursor and connection when done
                cursor.close()
                conn_ld.close()
            return 'ok'
        except sqlite3.Error as e:
            print('xx = ',e)
            return 'STUDENT_CHECKIN VIEW ERROR', 500
    else:
        return 'Database connection error', 500

@app.route('/student_checkout',methods=['GET','POST'])
def checkout():
    print(f'came in student_checkout')
    if request.method == 'GET':
        return render_template("/mess_checkin.html")
    
    # else its a post request
    conn_ld,conn_bf = create_connection_for_check_mess()
    if conn_ld is not None and conn_bf is not None:
        try:
            result = create_table_for_check_mess(conn1=conn_ld,conn2=conn_bf)
            if result =='fail':
                return 'TABLE LD AND BF CREATION ERROR', 500
            data = request.form # change to change.form
            print(f'data = {data}')
            user_id = session.get('user_id')
            meal_type = data['meal_type']
            # Get the current date
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            
            current_date_str = current_date.strftime('%Y-%m-%d')
            current_time_str = current_time.strftime('%H:%M:%S')
            if meal_type=='bf':
                cursor = conn_bf.cursor()
                sql_query = "SELECT * FROM BREAKFAST WHERE User_id = ? ORDER BY id DESC LIMIT 1" # select last entry of User_id
                # Execute the query with user_id=1
                cursor.execute(sql_query, (user_id,))
                # Fetch the result
                last_entry = cursor.fetchone()
                # Print or process the last entry
                print(f'le = ',last_entry)
                
                if last_entry is None:
                    return 'MESS ALREADY OUT',200
                else:
                    last_entry_date = datetime.strptime(last_entry[3], "%Y-%m-%d").date()
                    diff = (current_date - last_entry_date).days
                    print(f'diff = {diff}')
                    if current_time.hour > 20:
                        return 'NOT ALLOWED TO MESS OUT AFTER 11',200
                    elif last_entry[2]=='OUT':
                        return 'ALREADY MESS OUT',200
                    else:
                        counter = last_entry[5] + diff
                        cursor.execute('''INSERT INTO BREAKFAST (User_id, Check_status, Date,Time, Counter) VALUES (?, ?, ?, ?,?)''', (user_id,'OUT',current_date_str,current_time_str,counter))
                        conn_bf.commit()
                # Don't forget to close the cursor and connection when done
                cursor.close()
                conn_bf.close()
            elif meal_type=='ld':
                cursor = conn_ld.cursor()
                sql_query = "SELECT * FROM LD WHERE User_id = ? ORDER BY id DESC LIMIT 1" # select last entry of User_id
                # Execute the query with user_id=1
                cursor.execute(sql_query, (user_id,))
                # Fetch the result
                last_entry = cursor.fetchone()
                # Print or process the last entry
                print(f'last entry = {last_entry}')
                if last_entry is None:
                    return 'MESS ALREADY OUT',200
                else:
                    last_entry_date = datetime.strptime(last_entry[3], "%Y-%m-%d").date()
                    diff = (current_date - last_entry_date).days
                    print(f'diff = {diff}')
                    if current_time.hour > 20:
                        return 'NOT ALLOWED TO MESS OUT AFTER 11',200
                    elif last_entry[2]=='OUT':
                        return 'ALREADY MESS OUT',200
                    else:
                        counter = last_entry[5] + diff
                        cursor.execute('''INSERT INTO LD (User_id, Check_status, Date,Time,Counter) VALUES (?, ?, ?, ?,?)''', (user_id,'OUT',current_date_str,current_time_str,counter))
                        conn_ld.commit()
                # Don't forget to close the cursor and connection when done
                cursor.close()
                conn_ld.close()
            return 'ok'
        except sqlite3.Error as e:
            print('xx = ',e)
            return 'STUDENT_CHECKIN VIEW ERROR', 500
    else:
        return 'Database connection error', 500
    
@app.route('/student_check_messbill',methods=['GET','POST'])
def student_check_mess_bill():
    BF_PRICE = 100
    LD_PRICE = 200
    conn_ld,conn_bf = create_connection_for_check_mess()
    if conn_ld is not None and conn_bf is not None:
        user_id = session.get('user_id')
        cursor_bf = conn_bf.cursor()
        sql_query = "SELECT * FROM BREAKFAST WHERE User_id = ? ORDER BY id DESC LIMIT 1" # select last entry of User_id
        # Execute the query with user_id=1
        cursor_bf.execute(sql_query, (user_id,))
        # Fetch the result
        last_entry_bf = cursor_bf.fetchone()


        cursor_ld = conn_ld.cursor()
        sql_query = "SELECT * FROM LD WHERE User_id = ? ORDER BY id DESC LIMIT 1" # select last entry of User_id
        # Execute the query with user_id=1
        cursor_ld.execute(sql_query, (user_id,))
        # Fetch the result
        last_entry_ld = cursor_ld.fetchone()

        bf_check=True
        ld_check=True
        
        total_bf_days = 0
        total_ld_days = 0

        if last_entry_ld is None and last_entry_bf is None:
            return 'MESS WAS NOT IN. SO BILL IS 0',200
        elif last_entry_bf is None:
            bf_check=False
        elif last_entry_ld is None:
            ld_check=False

        if bf_check:
            last_entry_date_bf = datetime.strptime(last_entry_bf[3], "%Y-%m-%d").date()
        if ld_check:    
            last_entry_date_ld = datetime.strptime(last_entry_ld[3], "%Y-%m-%d").date()
        current_date = datetime.now().date()

        total_bf_price = 0
        total_ld_price = 0
        if bf_check and last_entry_bf[2]=='IN':
            last_entry_date_bf = datetime.strptime(last_entry_bf[3], "%Y-%m-%d").date()
            diff = (current_date-last_entry_date_bf).days

            total_bf_days = last_entry_bf[5]+diff

            total_bf_price = total_bf_days * BF_PRICE
        elif bf_check:
            total_bf_days = last_entry_bf[5]
            total_bf_price = last_entry_bf[5] * BF_PRICE
        
        if ld_check and last_entry_ld[2]=='IN':
            last_entry_date_ld = datetime.strptime(last_entry_ld[3], "%Y-%m-%d").date()
            diff = (current_date-last_entry_date_ld).days

            total_ld_days = last_entry_ld[5]+diff

            total_ld_price = total_ld_days * LD_PRICE
        elif ld_check:
            total_ld_days = last_entry_ld[5]
            total_ld_price = last_entry_ld[5] * LD_PRICE
        
        total_bill = total_bf_price + total_ld_price

        return f'total bill = {total_bill} because of {total_bf_days} Breakfasts and {total_ld_days} lunch&dinners',200
    else:
        return 'Database connection error', 500

@app.route('/display_menu')
def display_menu():
    u_type = session.get('User_Type')
    print(f'u_type = {u_type}')
    conn = create_connection_for_menu()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM menu')
            menu_data = cursor.fetchall()
            conn.close()
            return render_template('display_menu.html', menu_data=menu_data)
        except sqlite3.Error as e:
            print(e)
            return 'Failed to fetch menu data', 500
    else:
        return 'Database connection error', 500

@app.route('/display_menu_for_student')
def display_menu2():
    u_type = session.get('User_Type')
    print(f'u_type = {u_type}')
    conn = create_connection_for_menu()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM menu')
            menu_data = cursor.fetchall()
            conn.close()
            return render_template('display_menu_for_Student.html', menu_data=menu_data)
        except sqlite3.Error as e:
            print(e)
            return 'Failed to fetch menu data', 500
    else:
        return 'Database connection error', 500

  
@app.route("/create_menu")
def create_menu():
    return render_template("/create_menu.html")
@app.route('/create_menu_auth', methods=['POST'])
def create_menu_auth():
    conn = create_connection_for_menu()
    if conn is not None:
        create_table_for_menu(conn)
        day = request.form['day']
        breakfast = request.form['breakfast']
        lunch = request.form['lunch']
        dinner = request.form['dinner']
        try:
            cursor = conn.cursor()
            # Check if menu for the day already exists
            cursor.execute('''
                SELECT * FROM menu WHERE day = ?
            ''', (day,))
            existing_menu = cursor.fetchone()
            if existing_menu:
                return jsonify({'error': 'Menu for this day already exists '}), 400
            
            # If menu for the day doesn't exist, create a new one
            cursor.execute('''
                INSERT INTO menu (day, breakfast, lunch, dinner) VALUES (?, ?, ?, ?)
            ''', (day, breakfast, lunch, dinner))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Menu created successfully'}), 201
        except sqlite3.Error as e:
            conn.rollback()
            print(e)
            return jsonify({'error': 'Failed to create menu'}), 500
    else:
        return jsonify({'error': 'Database connection error'}), 500

    
@app.route('/menu/<int:menu_id>/update', methods=['GET', 'POST'])
def update_menu(menu_id):
    conn = create_connection_for_menu()
    if conn is not None:
        if request.method == 'GET':
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM menu WHERE id=?', (menu_id,))
                menu_data = cursor.fetchone()
                conn.close()
                return render_template('update_menu.html', menu_data=menu_data, menu_id=menu_id)
            except sqlite3.Error as e:
                print(e)
                return 'Failed to fetch menu data', 500
        elif request.method == 'POST':
            data = request.form
            day = data['day']
            breakfast = data['breakfast']
            lunch = data['lunch']
            dinner = data['dinner']
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE menu SET day=?, breakfast=?, lunch=?, dinner=? WHERE id=?
                ''', (day, breakfast, lunch, dinner, menu_id))
                conn.commit()
                conn.close()
                return redirect(url_for('display_menu'))
            except sqlite3.Error as e:
                print(e)
                return 'Failed to update menu', 500
    else:
        return 'Database connection error', 500
@app.route('/menu/<int:menu_id>/delete', methods=['GET'])
def delete_menu(menu_id):
    conn = create_connection_for_menu()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM menu WHERE id=?', (menu_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('display_menu'))
        except sqlite3.Error as e:
            print(e)
            return 'Failed to delete menu', 500
    else:
        return 'Database connection error', 500
# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
def get_db2():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE2)
    return db
def setup_Users():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        user_type TEXT DEFAULT 'Student',
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    db.commit()
    db.close()
def setup_reveiws():
    db = sqlite3.connect(DATABASE2)
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reveiws (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phonenumber INTEGER,
        email TEXT,
        concern TEXT ,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )       
    ''')
    db.commit()
    db.close()
@app.route('/studentreveiws', methods=['POST'])
def reveiws():
    setup_reveiws()  # Assuming this is a function to set up the database
    name = request.form['name']
    phonenumber = request.form['phone']
    email= request.form['email']
    text = request.form['text']
    db = get_db2()
    cursor = db.cursor()
    cursor.execute('INSERT INTO reveiws (name, phonenumber, email, concern) VALUES (?, ?, ?, ?)', (name, phonenumber, email, text))
    db.commit()
    return render_template("/Login/Sucess_Message.html")
# Function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/login")
def signin():
    return render_template("/Login/SignIn.html")
@app.route('/signup2', methods=['POST'])
def signup2():
    setup_Users()  # Assuming this is a function to set up the database
    name = request.form['Enter_name_for_signup']
    email = request.form['Enter_email_for_sigup']
    password = request.form['Enter_password_for_signup']
    user_type = request.form['Roles_SS']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        # Check if the user already exists
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        print(existing_user)
        if existing_user:
            flash('Account already exists!', 'error')
            return redirect(url_for('signup_function'))  # Redirect back to sign-up function
        else:
            # Insert the user data into the database
            cursor.execute('INSERT INTO users (name, email, password, user_type) VALUES (?, ?, ?, ?)', (name, email, hashed_password, user_type))
            db.commit()
            flash('Account created successfully!', 'success')
            return render_template("/Login/SignIn.html")
    except sqlite3.IntegrityError:
        flash('Error creating account!', 'error')
        return redirect(url_for('signup_function'))  # Redirect back to sign-up function
#SuperVisor Portion 
@app.route('/supervisorView')
def supervisorView():
    return render_template("/SuperVisorView.html")  
@app.route('/aboutus')
def aboutUs():
    # return render_template("/templates/AboutUs/aboutus.html")   
    return render_template("/AboutUs/Aboutus.html")    
#Student Portion 
@app.route('/studentView')
def studentView():
    return render_template("/StudentView.html")
@app.route('/studentReveiw')
def studentReview():
    return render_template("/review.html")
@app.route('/auth', methods=['POST'])
def auth():
    email = request.form['User_Email']
    password = request.form['User_Password']
    # Hash the provided password for comparison
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Retrieve user data from the database based on the email
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    session['user_id'] = user[0]
    # Check if user exists and passwords match
    session['User_Type'] = user[4]
    User_Type=session.get('User_Type')
    if user and user[3] == hashed_password:
        if User_Type=="Supervisor":
            
            return redirect(url_for("supervisorView"))
        else:
            return redirect(url_for("studentView"))
    else:
        flash('Invalid Email or Password Try Again!', 'error')
        return render_template("/Login/SignIn.html")

@app.route('/signup', methods=['GET'])
def signup_function():
    return render_template('/Login/signup.html')  # Render your sign-up page

@app.route("/signup")
def signup():
    return render_template("/Login/signup.html")

if __name__=='__main__':
    app.run(debug=True)