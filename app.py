from flask import Flask ,render_template,jsonify,request, redirect, url_for, g,session,flash
import time
import os
import hashlib
import sqlite3
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
        email TEXT UNIQUE,
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
        session.pop('_flashes', None)
        if existing_user:
            flash('Account already exists!', 'error')
            return redirect(url_for('signup_function'))  # Redirect back to sign-up function
        else:
            # Insert the user data into the database
            cursor.execute('INSERT INTO users (name, email, password, user_type) VALUES (?, ?, ?, ?)', (name, email, hashed_password, user_type))
            db.commit()
            flash('Account created successfully!', 'success')
            print("Hello")
            print(existing_user)
            if user_type=="Supervisor":
                return render_template("/display_menu.html")
            else:
                return f"Wellcome to {user_type} Webpage"# Redirect back to sign-up function
    except sqlite3.IntegrityError:
        flash('Error creating account!', 'error')
        return redirect(url_for('signup_function'))  # Redirect back to sign-up function
   
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
@app.route('/signup', methods=['GET'])
def signup_function():
    return render_template('/Login/signup.html')  # Render your sign-up page

@app.route("/signup")
def signup():
    return render_template("/Login/signup.html")

if __name__=='__main__':
    app.run(debug=True)