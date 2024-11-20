#!/usr/bin/env python3
"""
'auth.py' contains a function for passwords hashing
"""
from bcrypt import checkpw, gensalt, hashpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(pwd: str) -> bytes:
    """
    '_hash_password' hashes any string input password.
    """
    encoded_pwd = pwd.encode('utf-8')
    salt = gensalt()
    return (hashpw(encoded_pwd, salt))


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        'register_user' processes a user request for registration
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists.')
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return (user)

    def valid_login(self, email: str, pwd: str) -> bool:
        """
        'valid_login' matches a user's credential with the database.
        """
        try:
            user = self._db.find_user_by(email=email)
            return (checkpw(pwd.encode('utf-8'), user.hashed_password))
        except NoResultFound:
            return (False)
