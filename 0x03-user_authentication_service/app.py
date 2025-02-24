#!/usr/bin/env python3
""" A Simple flask app"""

from auth import Auth
from flask import (Flask, jsonify, request,
                   abort, make_response, redirect, url_for)
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

    if AUTH.valid_login(email, password) is False:
        abort(401)

    session_id = AUTH.create_session(email)

    response = make_response(jsonify({"email": email,
                                     "message": "logged in"}))

    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """The request is expected to contain the session ID as a cookie
    with key "session_id".

    Find the user with the requested session ID. If the user exists
    destroy the session and redirect the user to GET /. If the user does
    not exist, respond with a 403 HTTP status.
    """
    # get the session_id from request.cookies
    session_id = request.cookies.get("session_id")

    # using the session_id to get the actual user object
    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        # kill the session using the user id
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """The request is expected to contain a session_id cookie.
    Use it to find the user. If the user exist, respond with a
    200 HTTP status and the following JSON payload:
    {"email": "<user email>"}
    """
    session_id = request.cookies.get('session_id')

    # obtain user from the session id
    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """In this task, you will implement a get_reset_password_token function
    to respond to the POST /reset_password route.

    The request is expected to contain form data with the "email" field.

    If the email is not registered, respond with a 403 status code.
    Otherwise, generate a token and respond with a 200 HTTP status
    and the following JSON payload:
    """
    email = request.form.get('email')

    try:
        token = self._db.get_reset_password_token(email)
        response = jsonify({"email": email, "reset_token": token}), 200
        return response
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password():
    """The request is expected to contain form data with fields "email",
    "reset_token" and "new_password".

    Update the password. If the token is invalid, catch the exception
    and respond with a 403 HTTP code.

    If the token is valid, respond with a 200 HTTP code and the following
    JSON payload:
    """

    email = request.form.get('email')
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
