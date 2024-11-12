#!/usr/bin/env python3
"""
Route module for the API for this temporary usage of flask app
instal the depencies
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, abort
from werkzeug.exceptions import HTTPException
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler
def not_found() -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler
def unauthorized() -> str:
    """error handler, n this archive, you will find a simple
    API with one model: User. Storage of these users is done
    via a serialization/deserialization in files.
    """

    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
