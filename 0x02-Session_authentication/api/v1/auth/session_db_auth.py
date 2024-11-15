#!/usr/bin/env python3
"""The module for Session DB Auth"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from flask import request


class SessionDBAuth(SessionExpAuth):
    """The class SessionDBAuth that inherits from SessionExpAuth"""
    def create_session(self, user_id=None):
        """
        Method that creates and stores new instance of UserSession
        and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None or type(session_id) is not str:
            return None

        kwargs = {
            'user_id': user_id,
            'session_id': session_id
        }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Method that returns the User ID by requesting UserSession,
        in the database based on session_id
        """
        if session_id is None or type(session_id) is not str:
            return None

        sessions = UserSession.search({'session_id': session_id})
        if not sessions or len(sessions) <= 0:
            return none
        user_session = sessions[0]
        seshTime = timedelta(seconds=self.session_duration)
        expTime = user_session.created_at + seshTime
        if expTime < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Method that destroys the UserSession based on the Session ID,
        from the request cookie
        """
        session_id = self.session_cookie(request)
        if request is None or session_id is None or user_id is None:
            return False
        sessions = UserSession.search({'session_id': session_id})
        if not sessions or len(sessions) <= 0:
            return False
        for sesh in sessions:
            session.remove()
        return True
