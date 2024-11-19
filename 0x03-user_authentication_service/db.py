#!/usr/bin/env python3
"""
'db.py' complete the DB class provided below to implement the add_user method.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
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

    def find_user_by(self, **kwargs: str) -> User:
        """
        Retrieves the first record matching the input parameter.
        """
        fields, values = [], []

        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        user = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs: str) -> None:
        """
        Replaces old object values with new ones.
        """
        user = self.find_user_by(id=user_id)
        source = {}

        if user is None:
            return

        for key, value in kwargs.items():
            if hasattr(User, key):
                source[key] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            source,
            synchronize_session=False,
        )
        self._session.commit()
