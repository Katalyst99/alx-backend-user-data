#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello() -> str:
    """Returns a Jsonified Message when / is called"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
