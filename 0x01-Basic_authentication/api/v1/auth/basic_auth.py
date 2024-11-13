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
    pass
