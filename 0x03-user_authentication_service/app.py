#!/usr/bin/env python3
"""
'app.py' contains an authentication facilitating Flask app
"""
from auth import Auth
from flask import abort, Flask, jsonify, request


AUTH = Auth()

app = Flask(__name__)


@app.route('/')
def home():
    """
    'home' is the default route for the application.
    """
    return (jsonify({'message': 'Bienvenue'}))


@app.route('/users', methods=['POST'])
def users():
    """
    'users' is an endpoint handling user registration.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')

        try:
            user = AUTH.register_user(email, pwd)
            if user:
                return (jsonify({
                    'email': email,
                    'message': 'user created',
                }))
        except ValueError:
            return (jsonify({'message': 'email already registered'}), 400)


@app.route('/sessions', methods=['POST'])
def login():
    """
    'login' handles verification of signing in attempts.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')

        if AUTH.valid_login(email, pwd):
            session_id = AUTH.create_session(email)
            response = jsonify({'email': email,
                                'message': 'logged in'})
            response.set_cookie('session_id', session_id)
            return (response)

        abort(401)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
