#!/usr/bin/env python3
"""The module for implementing log filters to obfuscate PII"""
from typing import List
import re
import logging
import os
import mysql.connector


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Function that returns a connector to the database"""
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    db_connection = mysql.connector.connection.MySQLConnection(
        user=db_user,
        password=db_pwd,
        host=db_host,
        database=db_name
    )
    return db_connection


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


def main() -> None:
    """
    Obtains a database connection using get_db,
    and retrieve all rows in the users table,
    and display each row under a filtered format
    """
    db = get_db()
    cursor = db.cursor()
    qry = "SELECT * FROM users;"
    cursor.execute(qry)

    data = cursor.fetchall()
    fNames = [x[0] for x in cursor.description]

    logGer = get_logger()
    filtered = {'name', 'email', 'phone', 'ssn', 'password'}

    for r in data:
        msgLog = []
        for fld, val in zip(fNames, r):
            if fld in filtered:
                msgLog.append(f'{fld}=***')
            else:
                msgLog.append(f'{fld}={val}')

        logFmtd = "; ".join(msgLog)
        logGer.info(logFmtd)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
