#!/usr/bin/env python3
"""The module for Session Exp Auth"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from models.user import User
from datetime import datetime, timedelta
from flask import request


class SessionExpAuth(SessionAuth):
    """The class SessionExpAuth that inherits from SessionAuth"""

    def __init__(self):
        """Initializes the SessionExpAuth instance."""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Method that creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None or type(session_id) is not str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Method that returns a User ID based on a Session ID"""
        if session_id in self.user_id_by_session_id:
            seshDict = self.user_id_by_session_id[session_id]

            if self.session_duration <= 0:
                return seshDict['user_id']

            if 'created_at' not in seshDict:
                return None
            seshTime = timedelta(seconds=self.session_duration)
            expTime = seshDict['created_at'] + seshTime
            if expTime < datetime.now():
                return None
            return seshDict['user_id']
