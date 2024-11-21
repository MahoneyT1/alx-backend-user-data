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
from typing import Any
import uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """In this task, you will implement the Auth.valid_login method.
        It should expect email and password required arguments and return
        a boolean.

        Try locating the user by email. If it exists, check the password
        with bcrypt.checkpw. If it matches return True. In any other
        case, return False.
        """
        try:
            # using database method to find user with email
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """should return a string representation of a new
        UUID. Use the uuid
        module.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """ It takes an email string argument and returns the
        session ID as a string.The method should find the user
        corresponding to the email, generate a new UUID and store
        it in the database as the user’s session_id, then return the
        session ID.

        Remember that only public methods of self._db can be used.
        """
        user = None
        try:
            # find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        if user is None:
            return None

        # generate a uuid string
        session_id = self._generate_uuid()
        # update the user by inserting uuid_string in the session_id
        # column in the user schema database
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ It takes a single session_id string argument and returns
        the corresponding User or None.

        If the session ID is None or no user is found, return None.
        Otherwise return the corresponding user
        """

        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """The method updates the corresponding user’s session ID to None.
        """
        if user_id is None:
            return None

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Find the user corresponding to the email. If the user does not
        exist, raise a ValueError exception. If it exists, generate a
        UUID and update the user’s reset_token database field. Return
        the token.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()

            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except ValueError:
            raise

    def update_password(self, reset_token: str, password: str) -> None:
        """In this task, you will implement the Auth.update_password method.
        It takes reset_token string argument and a password string argument
        and returns None.

        Use the reset_token to find the corresponding user. If it does not
        exist, raise a ValueError exception.

        Otherwise, hash the password and update the user’s hashed_password
        field with the new hashed password and the reset_token field to None
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except ValueError:
            raise

        hashed_pass = _hash_password(password)
        self._db.update_user(hashed_password=hashed_pass, reset_token=None)
