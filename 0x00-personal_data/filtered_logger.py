#!/usr/bin/env python3
"""The module for implementing log filters to obfuscate PII"""
from typing import List
import re


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
