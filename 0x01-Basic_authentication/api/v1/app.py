#!/usr/bin/env python3

from ast import List
from email.policy import HTTP
from http.client import HTTPException
from os import getenv
from api.v1.views import app_views
from flask import Flask, Request, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

requests_paths = ['/api/v1/status/',
                  '/api/v1/unauthorized/',
                  '/api/v1/forbidden/']


@app.errorhandler(401)
def unauthorize_handler(e):
    """Route that triggers a 401 Unauthorized error.
    with the response of 401
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.before_request
def handle_before_request(r=requests_paths):
    """sets up the authorization system
    if environment varible is auth create auth instance
    Route module for the API, In this archive, you will find a simple
    API with one model: User. Storage of these users is done via a
    serialization/deserialization in files.
    """

    if os.getenv('AUTH_TYPE') == "basic_auth":
        from .auth.basic_auth import BasicAuth

        # Create an Instance of a Auth
        auth = BasicAuth()

        if auth is None:
            return

        result = auth.require_auth(request.path, r)
        if result is False:
            return

        result = auth.authorization_header(request)
        if result is None:
            abort(401)

        cur_user = auth.current_user(request)
        if cur_user is None:
            abort(403)

    elif os.getenv('AUTH_TYPE') == "auth":
        from .auth.auth import Auth
        auth = Auth()

        if auth is None:
            return

        result = auth.require_auth(request.path, r)
        if result is False:
            return

        result = auth.authorization_header(request)
        if result is None:
            abort(401)

        cur_user = auth.current_user(request)
        if cur_user is None:
            abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found error handler that handles eror 404 and response
    with error not found. Route module for the API, In this archive, you will find a simple
    API with one model: User. Storage of these users is done via a
    serialization/deserialization in files.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler for handling 403 errors
    triggered by abort() method of flask,
    Route module for the API, In this archive, you will find a simple
    API with one model: User. Storage of these users is done via a
    serialization/deserialization in files.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
