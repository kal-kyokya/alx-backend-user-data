#!/usr/bin/env python3
"""
Personal data
"""
import logging
import os
import re
from typing import List
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Replacing """
    for f in fields:
        message = re.sub(
            rf"{f}=(.*?)\{separator}",
            f'{f}={redaction}{separator}',
            message)
    return message


if __name__ == '__main__':
    main()
