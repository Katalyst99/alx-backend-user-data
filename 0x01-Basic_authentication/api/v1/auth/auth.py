#!/usr/bin/env python3
"""The module for a class to manage the API authentication."""
from typing import List, TypeVar
from flask import request


class Auth:
    """The authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to check if path needs authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """Public method to return authorization header from request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method to return current user from request"""
        return None
