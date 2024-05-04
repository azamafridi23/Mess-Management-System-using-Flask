from flask import Flask ,render_template,jsonify,request, redirect, url_for, g,session
import os
import hashlib
import sqlite3
from datetime import datetime
app=Flask(__name__)
app.secret_key = 'FullStackProject'
DATABASE = 'users.db'


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



@app.route('/student_checkin',methods=['POST'])
def checkin():
    print(f'came in student_checkin')
    conn_ld,conn_bf = create_connection_for_check_mess()
    if conn_ld is not None and conn_bf is not None:
        try:
            result = create_table_for_check_mess(conn1=conn_ld,conn2=conn_bf)
            if result =='fail':
                return 'TABLE LD AND BF CREATION ERROR', 500
            data = request.json # change to change.form
            print(f'data = {data}')
            user_id = data['user_id']
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
                    if current_time.hour > 11:
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
                    if current_time.hour > 11:
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
    
@app.route('/student_checkout',methods=['POST'])
def checkout():
    print(f'came in student_checkout')
    conn_ld,conn_bf = create_connection_for_check_mess()
    if conn_ld is not None and conn_bf is not None:
        try:
            result = create_table_for_check_mess(conn1=conn_ld,conn2=conn_bf)
            if result =='fail':
                return 'TABLE LD AND BF CREATION ERROR', 500
            data = request.json # change to change.form
            print(f'data = {data}')
            user_id = data['user_id']
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
                    if current_time.hour > 11:
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
                    if current_time.hour > 11:
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

def setup_Users():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        user_type TEXT DEFAULT 'Student',
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    db.commit()
    db.close()

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
    setup_Users()
    name = request.form['Enter_name_for_signup']
    email = request.form['Enter_email_for_sigup']
    password = request.form['Enter_password_for_signup']
    User_Types=request.form['Roles_SS']
    # Hash the password before storing it
    print(User_Types)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        # Insert the user data into the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (name, email, password,user_type) VALUES (?, ?, ?,?)', (name, email, hashed_password,User_Types))
        db.commit()
       # return redirect(url_for('login'))
        return render_template("/Login/accountcreation.html")
    except sqlite3.IntegrityError:
        return render_template("/Login/AccountExist.html")
    
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
    # Check if user exists and passwords match
    session['User_Type'] = user[4]
    User_Type=session.get('User_Type')
    if user and user[3] == hashed_password:
        if User_Type=="Supervisor":
            
            return render_template("/display_menu.html")
        else:
            return User_Type
    else:
        return render_template("/Login/Invalidemail.html")

@app.route("/signup")
def signup():
    return render_template("/Login/signup.html")

if __name__=='__main__':
    app.run(debug=True)