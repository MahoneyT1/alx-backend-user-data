#!/usr/bin/env python3
"""In this task you will define a _hash_password method that
takes in a password string arguments and returns bytes.

The returned bytes is a salted hash of the input password, hashed
with bcrypt.hashpw.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """converts string password to hashed
    Args:
        password(string)

    Returns:
        hashed password
    """
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers user
        Args:
            email(string) email to register a user
            password(string) to secure user registered

        Returns:
            User(object) returns user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pass = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pass)
            return new_user
