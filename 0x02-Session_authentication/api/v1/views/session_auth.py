#!/usr/bin/env python3
"""The module of session_auth views"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
       Return:
      - User object JSON represented
    """
    email = request.form.get('email')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None or email == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            seshId = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            resp.set_cookie(getenv('SESSION_NAME'), seshId)
            return resp
    return jsonify({"error": "wrong password"}), 401


@app_views.route('auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /api/v1/auth_session/logout
    Return:
        - Empty  JSON dictionary with the status code 200
    """
    from api.v1.app import auth
    seshDestroyed = auth.destroy_session(request)
    if not seshDestroyed:
        abort(404)
    return jsonify({}), 200
