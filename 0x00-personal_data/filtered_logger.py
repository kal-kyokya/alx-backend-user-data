#!/usr/bin/env python3
"""
Personal data
"""
import logging
import os
import re
from typing import List
import mysql.connector


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ Replacing """
    for f in fields:
        message = re.sub(
            rf"{f}=(.*?)\{separator}",
            f'{f}={redaction}{separator}',
            message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        """Constructor function for all class instances."""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records."""
        return filter_datum(self.fields, self.REDACTION,
                     super().format(record), self.SEPARATOR)


if __name__ == '__main__':
    main()
