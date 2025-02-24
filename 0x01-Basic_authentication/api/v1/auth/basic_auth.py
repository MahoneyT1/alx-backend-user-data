#!/usr/bin/env python3
"""Create a class BasicAuth that inherits from Auth. For the moment this
class will be empty. Update api/v1/app.py for using BasicAuth class instead
of Auth depending of the value of the environment variable
AUTH_TYPE, If AUTH_TYPE is equal to basic_auth:

import BasicAuth from api.v1.auth.basic_auth
create an instance of BasicAuth and assign it to the variable auth
"""
from ast import Tuple
from ctypes import Union
from pickle import NONE
from re import search
import re
from site import USER_BASE
from .auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Auth AUTH_TYPE, If AUTH_TYPE is equal to basic_auth:
    import BasicAuth from api.v1.auth.basic_auth
    create an instance of BasicAuth and assign it to the variable auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Add the method def extract_base64_authorization_header
        (self, authorization_header: str) -> str: in the class BasicAuth
        that returns the Base64 part of the Authorization header for a
        Basic Authentication:Return None if authorization_header is None
        Return None if authorization_header is not a string
        Return None if authorization_header doesn’t start by Basic
        (with a space at the end)
        Otherwise, return the value after Basic (after the space)
        You can assume authorization_header contains only one Basic
        """

        if not isinstance(
                          authorization_header,
                          str) or authorization_header is None:
            return None

        if authorization_header.startswith('Basic'):
            if " " in authorization_header:
                get_index = authorization_header.index(" ")

                new_string = authorization_header[get_index:]
                return new_string
            return None
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """that returns the decoded value of a Base64 string
        base64_authorization_header:
        Return None if base64_authorization_header is None
        Return None if base64_authorization_header is not a string
        Return None if base64_authorization_header is not a valid
        Base64 - you can use try/except
        Otherwise, return the decoded value as UTF8 string - you
        can use decode('utf-8')
        """

        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            new_decoded = base64.b64decode(base64_authorization_header)
            return new_decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str)\
            -> Tuple[str, str]:
        """BasicAuth that returns the user email and password from the Base64
        decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if isinstance(decoded_base64_authorization_header, str):
            if ":" in decoded_base64_authorization_header:
                decoded_email, password = tuple(
                    decoded_base64_authorization_header.split(':'))
                return decoded_email, password
            return (None, None)
        else:
            return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """asicAuth that returns the User instance based
        on his email and password"""

        # Return None if user_email is None or not a string
        if user_email is None:
            return None

        # Return None if user_pwd is None or not a string
        if type(user_pwd) is not str:
            return None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """BasicAuth that returns the User instance based on
        his email and password.
        Return None if user_email is None or not a string
        Return None if user_pwd is None or not a string
        """

        # Return None if user_email is None or not a string
        if type(user_email) is str and type(user_pwd) is str:
            try:
                users = User.search({"email": user_email})
            except Exception:
                return None

            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Now, you have all pieces for having a complete
        Basic authentication.
        You must use authorization_header
        You must use extract_base64_authorization_header
        You must use decode_base64_authorization_header
        You must use extract_user_credentials
        You must use user_object_from_credentials
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
