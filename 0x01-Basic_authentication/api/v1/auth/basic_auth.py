#!/usr/bin/env python3
"""Create a class BasicAuth that inherits from Auth. For the moment this
class will be empty. Update api/v1/app.py for using BasicAuth class instead
of Auth depending of the value of the environment variable
AUTH_TYPE, If AUTH_TYPE is equal to basic_auth:

import BasicAuth from api.v1.auth.basic_auth
create an instance of BasicAuth and assign it to the variable auth
"""
from .auth import Auth


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

        if not isinstance(authorization_header, str) or authorization_header is None:
            return None

        if authorization_header.startswith('Basic'):
            if " " in authorization_header:
                get_index = authorization_header.index(" ")

                new_string = authorization_header[get_index:]
                return new_string
