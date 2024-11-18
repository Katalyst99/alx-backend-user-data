#!/usr/bin/env python3
"""The module for authentication"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Method that takes in a password argument and returns a salted,
    hashed password.
    """
    hashedPwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashedPwd
