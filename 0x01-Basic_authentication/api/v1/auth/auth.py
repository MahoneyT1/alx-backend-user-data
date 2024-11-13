#!/usr/bin/env python3
""" Returns False - path and excluded_paths will be used later,
now, you don’t need to take care of them

public method def authorization_header(self, request=None) -> str:
that returns None - request will be the Flask request object
public method def current_user(self, request=None)
-> TypeVar('User'): that returns
None - request will be the Flask request object
This class is the template for all authentication system you
will implement.
"""
from flask import request
from typing import List, TypeVar
import re
from flask import request, abort

from api.v1 import auth


class Auth:
    """Authentication system for the Api"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Update the method def require_auth, that returns True if the path
        is not in the list of strings excluded_paths:

        Returns True if path is None
        Returns True if excluded_paths is None or empty
        Returns False if path is in excluded_paths
        You can assume excluded_paths contains string path always ending by a /
        This method must be slash tolerant: path=/api/v1/status and
        path=/api/v1/status/ must be returned False if excluded_paths
        contains /api/v1/status/
        """

        if path is not None and excluded_paths is not None:
            for excluded_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ""

                if excluded_path[-1] == '*':
                    pattern = "{}.*".format(excluded_path[0:-1])

                elif excluded_path[-1] == '/':
                    pattern = "{}/*".format(excluded_path[0:-1])

                else:
                    pattern = "{}/*".format(excluded_path)

                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ If request is None, returns None
        If request doesn’t contain the header key Authorization, returns None
        Otherwise, return the value of the header request Authorization
        Update the file api/v1/app.py:""
        return None
        """

        if request is None:
            return None

        authorization = request.headers.get('Authorization')

        if authorization is None:
            return None
        else:
            return authorization 


    
    def current_user(self, request=None) -> TypeVar:
        """stores the current user """
        user  = re
