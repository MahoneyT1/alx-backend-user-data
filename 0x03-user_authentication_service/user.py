#!/usr/bin/env python3
"""In this task you will create a SQLAlchemy model named User
for a database table named users (by using the mapping
declaration of SQLAlchemy).
The model will have the following attributes:

id, the integer primary key
email, a non-nullable string
hashed_password, a non-nullable string
session_id, a nullable string
reset_token, a nullable string
"""

from sqalachemy.declarative.ext import declarative_base
from sqalachemy import Column, Integer, String


base = declarative_base()


class User(base):
    """User table that maps id, email, password, session, token_reset
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
