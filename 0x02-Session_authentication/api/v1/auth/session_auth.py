#!/usr/bin/env python3
"""The module for Session Auth"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method that returns a User ID based on a Session ID"""
        if session_id is None or type(session_id) is not str:
            return None
        else:
            userId = self.user_id_by_session_id.get(session_id)
        return userId

    def current_user(self, request=None):
        """Method that returns a User instance based on a cookie value"""
        seshId = self.session_cookie(request)
        userId = self.user_id_for_session_id(seshId)
        return User.get(userId)

    def destroy_session(self, request=None):
        """Method that deletes the user session / logout"""
        seshId = self.session_cookie(request)
        userId = self.user_id_for_session_id(seshId)
        if request is None or seshId is None or userId is None:
            return False
        else:
            del self.user_id_by_session_id[seshId]
        return True
