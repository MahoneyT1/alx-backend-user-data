#!/usr/bin/env python3

"""
Write a function called filter_datum that returns the log message obfuscated:

Arguments:
fields: a list of strings representing all fields to obfuscate
redaction: a string representing by what the field will be obfuscated
message: a string representing the log line
separator: a string representing by which character is separating all
fields in the log line (message)
The function should use a regex to replace occurrences of certain field values.
filter_datum should be less than 5 lines long and use re.sub to perform the
substitution with a single regex.
"""
from typing import List
import logging
import re


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """using regex to match group of patterns"""

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

    def __init__(self, fields: List[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """Implement the format method to filter values in incoming log records
        """
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)
