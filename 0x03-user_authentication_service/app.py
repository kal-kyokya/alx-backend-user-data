#!/usr/bin/env python3
"""
'app.py' contains an authentication facilitating Flask app
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def home():
    """
    'home' is the default route for the application.
    """
    return (jsonify({'message': 'Bienvenue'}))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
