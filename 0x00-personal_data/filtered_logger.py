#!/usr/bin/env python3
"""Obfuscates specified fields in a log message.
Args:
    fields (List[str]): List of field names to obfuscate.
    redaction (str): String to replace sensitive field values with.
    message (str): The log message containing sensitive data.
    separator (str): Character that separates fields in the log message.
Returns:
    str: The obfuscated log message.
"""

from typing import List
import logging
import re
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'name')


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """Initialize the formatter with fields to redact.
    Args:
        fields (List[str]): Fields to redact in log messages.
    """
    pattern = r"(" + "|".join(re.escape(field) + r"=[^" + re.escape(separator)
                              + r"]+" for field in fields) + r")"

    # Replace each sensitive field match with `field=[REDACTED]`
    redacted_message = re.sub(pattern,
                              lambda match: match.group(0).split('=')[0]
                              + "=" + redaction, message)

    return redacted_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION: str = "***"
    FORMAT: str =\
        "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR: str = ";"

    def __init__(self, fields: List[str]):
        """initialize an instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """Implement the format method to filter values in incoming log records
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


def get_logger() -> logging.Logger:
    """Implement a get_logger function that takes no arguments and returns a
    logging.Logger object.

    The logger should be named "user_data" and only log up to logging.INFO
    level. It should not propagate messages to other loggers. It should
    have a StreamHandler with RedactingFormatter as formatter.
    """

    # Create a logger with the name user_data
    logger = logging.getLogger('user_data')
    # Set logger level to Info
    logger.setLevel(logging.INFO)

    # Create the logger_handler streamhandleer for streaming stdout to console
    logger_handler = logging.StreamHandler()
    logger_handler.setFormatter(RedactingFormatter.FORMAT)
    logger.addHandler(logger_handler)
    logger.propagate = False
    return logger


def get_db() -> MySQLConnection:
    """function that returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).

    Use the os module to obtain credentials from the environment
    Use the module mysql-connector-python to connect to the MySQL
    database
    """

    # exract the environmenet variabls for mysql connector object
    conn_obj = mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        username=os.getenv("PERSONAL_DATA_DB_USERNAME"),
        port=3306
    )
    return conn_obj
