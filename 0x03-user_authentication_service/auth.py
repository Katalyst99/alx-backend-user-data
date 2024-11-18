#!/usr/bin/env python3
"""The module for authentication"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound

from user import User


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
