#!/usr/bin/env python3
""" Route module for the API, In this archive, you will find a simple
API with one model: User. Storage of these users is done via a
serialization/deserialization in files.
"""
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


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_route(e) -> str:
    """forbidden error handler"""
    data = {
        "error": "Forbidden"
    }
    return jsonify(data), 403


"""Add a method in api/v1/app.py to handler before_request
if auth is None, do nothing
if request.path is not part of this list
['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'],
do nothing - you must use the method require_auth from the auth instance
if auth.authorization_header(request) returns None, raise the error 401
- you must use abort if auth.current_user(request) returns None, raise
the error 403 - you must use abort
"""

requests_paths = ['/api/v1/status/',
                  '/api/v1/unauthorized/',
                  '/api/v1/forbidden/']

if os.getenv('AUTH_TYPE') == "auth":
    from api.v1.auth.auth import Auth

    # Create an Instance of  a Auth
    auth = Auth()

    if auth is None:
        pass


def handle_before_request(req_p, requests_paths):
    """sets up the authorization system"""
    if request.paths in requests_paths:
        pass

    result = auth.authorization_header(request)
    if result is None:
        abort(401)

    cur_user = auth.current_user(request)

    if cur_user is None:
        abort(403)

    result = auth.authorization_header(request)
    if result is None:
        abort(401)

    cur_user = auth.current_user(request)

    if cur_user is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
