#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
import logging
from typing import Dict, Mapping, Any


logging.disable(logging.CRITICAL)


class DB:
    """DB class for database, creates and tears down db at the point of
    entry
    """

    def __init__(self) -> None:
        """Initialize a new DB instance, create the engine and metada
        and create a session object set it to None
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """Implement the add_user method, which has two required
        string arguments: email and hashed_password, and returns
        a User object. The method should save the user to the database.
        No validations are required at this stage.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """This method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered by the method’s
        input arguments
        """
        try:
            # if not kwargs:
            #     raise InvalidRequestError("No filter criteria provided.")
            result = self._session.query(User).filter_by(**kwargs).first()

            if result is None:
                raise NoResultFound
            return result
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """method that takes as argument a required user_id integer
        and arbitrary keyword arguments, and returns None.
        Args:
            user_id to filter user by their id
        Returns:
            None
        The method will use find_user_by to locate the user to update,
        then will update the user’s attributes as passed in the method’s
        arguments then commit changes to the database.
        """
        user = self.find_user_by(id=user_id)

        try:
            user
            # find user by id
        except NoResultFound:
            raise ValueError

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        # commit to database
        self._session.commit()
        try:
            user = self.find_user_by(id=user_id)

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
       
                raise ValueError
        except NoResultFound:
            raise ValueError
        self._session.commit()
