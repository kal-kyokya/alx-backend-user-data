#!/usr/bin/env python3
"""
'db.py' complete the DB class provided below to implement the add_user method.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    'DB' class definition
    """

    def __init__(self) -> None:
        """
        Constructor method to Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Getter for the Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_pwd: str) -> User:
        """
        'add_user' saves the input user to the database.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_pwd)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return (new_user)
