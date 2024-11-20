#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method should save the user to the database"""
        userNew = User(email=email, hashed_password=hashed_password)
        self._session.add(userNew)
        self._session.commit()
        return userNew

    def find_user_by(self, **kwargs) -> User:
        """
        Method takes in arbitrary keyword arguments and returns the first row,
        found in the users table as filtered by the method’s input arguments
        """
        if not kwargs:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Method that takes as argument a required user_id integer,
        and arbitrary keyword arguments.
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise ValueError
        self._session.commit()
        return None
