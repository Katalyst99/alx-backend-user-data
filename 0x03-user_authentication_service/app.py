#!/usr/bin/env python3
""" Starts a Flash Web Application """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """Returns a Jsonified Message when / is called"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Function that implements the POST /users route."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Function to respond to the POST /sessions route."""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie('session_id', session_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Function to respond to the DELETE /sessions route."""
    seshId = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(seshId)
    if seshId is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Function to respond to the GET /profile route."""
    seshId = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(seshId)
    if seshId is None or user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Function to respond to the POST /reset_password route."""
    email = request.form.get('email')
    emailRegd = AUTH.create_session(email)
    if not emailRegd:
        abort(403)
    else:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Function to respond to the PUT /reset_password route."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
