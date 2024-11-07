#!/usr/bin/env python3
"""The module for encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Function that expects one string argument and  returns a salted,
    hashed password.
    """
    hashedPwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashedPwd
