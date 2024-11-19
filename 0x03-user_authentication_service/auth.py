#!/usr/bin/env python3
"""
'auth.py' contains a function for passwords hashing
"""
from bcrypt import gensalt, hashpw


def _hash_password(pwd: str) -> str:
    """
    '_hash_password' hashes any string input password.
    """
    encoded_pwd = pwd.encode()
    salt = gensalt()
    return (hashpw(encoded_pwd, salt))
