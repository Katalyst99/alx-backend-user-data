#!/usr/bin/env python3
"""The module for implementing log filters to obfuscate PII"""
from typing import List
import re
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Function should use a regex to replace occurrences of certain field values
    and returns the log message obfuscated
    """
    for fld in fields:
        rgx = f"(?<={fld}=)[^{separator}]*"
        message = re.sub(rgx, redaction, message)
    return message


def get_logger() -> logging.Logger:
    """Function that akes no arguments and returns a logging.Logger object."""
    logGer = logging.getLogger('user_data')
    logGer.setLevel(logging.INFO)
    logGer.propagate = False

    strmHandler = logging.StreamHandler()
    strmHandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logGer.addHandler(strmHandler)
    return logGer


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Method to filter values in incoming log records using filter_datum
        """
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
