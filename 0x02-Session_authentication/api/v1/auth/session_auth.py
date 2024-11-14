#!/usr/bin/env python3
"""The module for Session Auth"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """The SessionAuth class that inherits from Auth."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Method that creates a Session ID for a user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        else:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
        return session_id
