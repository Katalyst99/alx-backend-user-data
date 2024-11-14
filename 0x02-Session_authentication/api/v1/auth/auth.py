#!/usr/bin/env python3
"""The module for a class to manage the API authentication."""
from typing import List, TypeVar
from flask import request
from os import getenv


class Auth:
    """The authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to check if path needs authentication"""
        if path is None or not excluded_paths or excluded_paths is None:
            return True
        if not path.endswith('/'):
            path += '/'

        for excluPath in excluded_paths:
            if excluPath.endswith('*'):
                if path.startswith(excluPath[:-1]):
                    return False
            else:
                if not excluPath.endswith('/'):
                    excluPath += "/"
                if path in excluPath:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Public method to return authorization header from request"""
        if request is None:
            return None

        autHeader = request.headers.get('Authorization')
        return autHeader

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method to return current user from request"""
        return None

    def session_cookie(self, request=None):
        """Method that returns a cookie value from a request"""
        if request is None:
            return None

        cookieName = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(cookieName)
