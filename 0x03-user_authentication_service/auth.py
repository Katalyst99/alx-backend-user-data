#!/usr/bin/env python3
"""The module for authentication"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union
from user import User


def _generate_uuid() -> str:
    """Function should return a string representation of a new UUID"""
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """
    Method that takes in a password argument and returns a salted,
    hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Method should take mandatory email and password string arguments,
        and return a User object.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            userNew = self._db.add_user(email, _hash_password(password))
        return userNew

    def valid_login(self, email: str, password: str) -> bool:
        """
        Method should expect email and password required arguments,
        and return a boolean.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        Method should find the user corresponding to the email,
        generate a new UUID and store it in the database as the user’s,
        session_id. then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Method takes a single session_id string argument,
        and returns the corresponding User or None.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Method updates the corresponding user’s session ID to None.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Method take an email string argument and returns a string."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        user.reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=user.reset_token)
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Method takes reset_token string argument and,
        a password string argument and returns None.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
        return None
