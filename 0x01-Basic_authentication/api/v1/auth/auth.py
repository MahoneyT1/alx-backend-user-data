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


class Auth:
    """Authentication system for the Api"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Just returns false for the moment"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns False"""
        return None

    def current_user(self, request=None) -> TypeVar:
        """stores the current user """
        return None
