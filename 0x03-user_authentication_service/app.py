#!/usr/bin/env python3
""" A Simple flask app"""

from auth import Auth
from flask import Flask, jsonify, request, abort, make_response
from typing import Dict


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def home():
    """home page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user():
    """Register User route
    """
    # extract email and password from request form
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': user.email,
                        "message": "user created"
                        }), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """The request is expected to contain form data with "email"
    and a "password" fields.

    If the login information is incorrect, use flask.abort to respond
    with a 401 HTTP status
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email and not password:
        abort(401)

    session_id = AUTH.create_session(email)

    response = make_response(jsonify({"email": email,
                                     "message": "logged in"}))

    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
