#!/usr/bin/env python3
"""The module for a class to manage the API authentication."""
from typing import List, TypeVar
from flask import request


class Auth:
    """The authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to check if path needs authentication"""
        if path is None or not excluded_paths or excluded_paths is None:
            return True
        if not path.endswith('/'):
            path += '/'

        for excluPath in excluded_paths:
            if excluPath.endswith('/') and path in excluPath:
                return False
            elif not excluPath.endswith('/') and path in excluPath + "/":
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Public method to return authorization header from request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method to return current user from request"""
        return None