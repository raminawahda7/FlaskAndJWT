# app.py

from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt

from config import SECRET_KEY
from utils import connect_to_database

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

def token_required(func):
    def decorated(*args, **kwargs):
        if session.get('logged_in'):
            return jsonify({'message': 'Already logged in'}), 200
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        return func(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently'

@app.route('/public')
def public():
    return 'For Public'

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard!'

@app.route('/login', methods=['POST'])
def login():
    if session.get('logged_in'):
        return jsonify({'message': 'Already logged in'}), 200
    connection = connect_to_database()
    if not connection:
        return jsonify({'message': 'Database connection failed'}), 500
    #TODO: use orm like SQLAlchemy to access the database using query like LINQ
    email = request.json.get('email')
    password = request.json.get('password')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user and user[2] == password:
        session['logged_in'] = True
        token = jwt.encode({
            'user': email,
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
        app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'message': 'Login successful!', 'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    connection.close()

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'message': 'Successfully logged out!'})

if __name__ == "__main__":
    app.run(debug=True)
