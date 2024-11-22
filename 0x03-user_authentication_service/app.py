#!/usr/bin/env python3
"""
'app.py' contains an authentication facilitating Flask app
"""
from auth import Auth
from flask import abort, Flask, jsonify, redirect, request


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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    'logout' handles termination of ongoing sessions.
    """
    if request.method == 'DELETE':
        session_id = str(request.cookies.get('session_id'))
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        abort(403)


@app.route('/profile')
def profile():
    """
    'profile' retrieves a user off of the request cookie.
    """
    session_id = str(request.cookies.get('session_id'))
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return (jsonify({'email': user.email}))
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Ease access to reset password token
    """
    if request.method == 'POST':
        email = request.form.get('email')
        session_id = AUTH.create_session(email)
        if session_id:
            token = AUTH.get_reset_password_token(email)
            return (jsonify({'email': email,
                             'reset token': token}), 200)
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password

    Return:
        - The user's password updated payload.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    password_was_changed = False
    try:
        AUTH.update_password(reset_token, new_password)
        password_was_changed = True
    except ValueError:
        password_was_changed = False
    if password_was_changed:
        return jsonify({"email": email, "message": "Password updated"})
    abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
