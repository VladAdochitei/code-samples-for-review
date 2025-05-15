from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_socketio import SocketIO, send
import eventlet

# Add a global list to store online users
online_users = []

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from werkzeug.security import generate_password_hash, check_password_hash

import time
import sqlite3

conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')
conn.commit()

eventlet.monkey_patch()

app = Flask(__name__)
app.config["SECRET"] = 'fkhbekhbfewkhbk'
app.config["SECRET_KEY"] = "dwlnnojwdojweorh223rih52o3u5o32"

socketio = SocketIO(app, cors_allowed_origins="*")

# form
class MessageForm(FlaskForm):
    message  = StringField("Message", validators = [DataRequired()], render_kw={"id": "message"})
    submit   = SubmitField("Submit", render_kw={"id": "sendBtn"})

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=40)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, field):
        cursor.execute("SELECT id FROM users WHERE username=?", (field.data,))
        existing_user = cursor.fetchone()
        if existing_user:
            raise ValidationError("Username already taken. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], password):  # user[2] is the password_hash column
            session['user_id'] = user[0]  # Store user_id in the session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)  # Remove the user_id from the session
        flash('Logged out successfully!', 'success')
    if 'is_admin' in session: 
        session.pop('is_admin', None)
        flash('Successfully terminated Admin session', 'success')
    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(message):
    start = time.time()
    print("Received message: " + message)
    if message != "User connected!":
        user_message = message.split(': ')
        username = user_message[0]
        message_content = user_message[1]

        cursor.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message_content))
        conn.commit()

        send(message, broadcast=True)
    end = time.time()
    print(f"Elapsed time: {end - start}")


@app.route('/', methods=["GET", "POST"])
def index():
    # Check if the user is authenticated (logged in)
    if 'user_id' not in session:
        flash('Please log in to access the chat.', 'warning')
        return redirect(url_for('login'))

    # Fetch the username from the session
    user_id = session['user_id']
    cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
    user = cursor.fetchone()
    if user:
        username = user[0]
        print(f'parsed username is {username}')
    else:
        username = 'Guest'

    form = MessageForm()

    # Emit the 'online_users' event to update the online user list
    update_online_users()

    if request.method == "POST" and form.validate_on_submit():
        # Code executed after the form is validated
        message = form.message.data

        # Use the username fetched from the session
        socketio.emit('submit_message', {'username': username, 'message': message}, broadcast=True)


        # Store the message in the database
        cursor.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message))

        conn.commit()

    # Load messages from the database
    messages = load_messages_from_db()

    return render_template("index.html", form=form, messages=messages, username=username)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    cursor.execute('SELECT id, username FROM users')  # Fetch all users
    users = cursor.fetchall()
    return render_template('admin.html', users=users)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_password = request.form.get('password')
        if admin_password == 'admin_123456':
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('admin_login.html')


def load_messages_from_db():
    cursor.execute('SELECT * FROM messages ORDER BY timestamp ASC')  # Fetch messages in ascending order
    messages = cursor.fetchall()
    return reversed(messages)  # Reverse the list to display latest messages at the bottom


# Modify the connection and disconnection handlers to update the list
@socketio.on('connect')
def handle_connect():
    username = get_username()
    if username not in online_users:
        online_users.append(username)
    update_online_users()

@socketio.on('disconnect')
def handle_disconnect():
    username = get_username()
    if username in online_users:
        online_users.remove(username)
    update_online_users()

def update_online_users():
    socketio.emit('online_users', {'users': online_users})

# There is a bug in here, first user always gets rendered as Guest!
def get_username():
    if 'user_id' in session:
        print(session)
        user_id = session['user_id']
        cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
        user = cursor.fetchone()
        if user:
            print(f'------------>{user[0]}')
            return user[0]
    print(session)
    return 'Guest'

import csv
from flask import Response, abort

# Add a new route for downloading message history in CSV format
@app.route('/download/messages.csv', methods=['GET'])
def download_messages_csv():
    if not session.get('is_admin'):
        abort(403)  # 403 Forbidden if not admin
    # Fetch messages from the database
    messages = load_messages_from_db()
    
    # Define the headers for the CSV file
    headers = ['ID', 'Username', 'Message', 'Timestamp']
    
    # Create a CSV string
    csv_data = ','.join(headers) + '\n'
    for message in messages:
        csv_data += ','.join(map(str, message)) + '\n'
    
    # Set response headers
    headers = {
        "Content-Disposition": "attachment; filename=messages.csv",
        "Content-Type": "text/csv"
    }
    
    # Return CSV file as response
    return Response(
        csv_data,
        status=200,
        headers=headers
    )

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('is_admin'):
        abort(403)  # 403 Forbidden if not admin
    
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin'))



if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)