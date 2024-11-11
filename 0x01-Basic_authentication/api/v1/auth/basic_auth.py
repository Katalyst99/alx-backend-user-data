#!/usr/bin/env python3
"""The module for Basic auth"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """The basicAuth class that inherits from Auth."""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Method that returns the Base64 part of the Authorization header,
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Method that returns the decoded value of,
        a Base64 string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decodeVal = base64.b64decode(base64_authorization_header)
            return decodeVal.decode('utf-8')
        except BaseException:
            return None
