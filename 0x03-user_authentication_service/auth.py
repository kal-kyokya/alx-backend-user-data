#!/usr/bin/env python3
"""
'auth.py' contains a function for passwords hashing
"""
from bcrypt import checkpw, gensalt, hashpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """
    '_hash_password' hashes any string input password.
    """
    encoded_password = password.encode('utf-8')
    salt = gensalt()
    return (hashpw(encoded_password, salt))


def _generate_uuid() -> str:
    """
    '_generate_uuid' returns a string representation of a uuid.
    """
    return (str(uuid.uuid4()))


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
        'valid_login' verifies a user's credential prior to signing in.
        """
        try:
            user = self._db.find_user_by(email=email)
            return (checkpw(pwd.encode('utf-8'), user.hashed_password))
        except NoResultFound:
            return (False)

    def create_session(self, email: str) -> str:
        """
        'create_session' assigns a session ID to a specific user.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return (user.session_id)
        except NoResultFound:
            return (None)

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Returns a user off of its session ID.
        """
        if not session_id:
            return (None)
        try:
            return (self._db.find_user_by(session_id=session_id))
        except NoResultFound:
            return (None)

    def destroy_session(self, user_id: int) -> None:
        """
        'destroy_session' terminates a user's session.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return (user.session_id)
        except NoResultFound:
            return (None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Create a reset password token for email associated.
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            user.reset_token = token
            return (token)
        except NoResultFound:
            raise ValueError
