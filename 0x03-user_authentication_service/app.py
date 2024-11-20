#!/usr/bin/python3
""" A Simple flask app"""

from flask import flask, jsonify


app = Flask(__name__)


@app.route("/", method=['GET'], strict_slashes=False)
def home():
    """home page"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
