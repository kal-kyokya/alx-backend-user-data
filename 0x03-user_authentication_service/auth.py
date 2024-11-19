#!/usr/bin/env python3
"""
'auth.py' contains a function for passwords hashing
"""
from bcrypt import gensalt, hashpw


def _hash_password(pwd):
    """
    '_hash_password' hashes any string input password.
    """
    salt = gensalt()
    return (hashpw(pwd.encode(), salt))
