# -*- coding: utf-8 -*-
"""
Exceptions

The base exception class is :errors:`.CoreError`.

"""


class CoreError(Exception):

    """Father of errors."""


class DBConnectionError(CoreError):

    """Raise when there are problems when connecting to the databaseserver."""


class DBError(CoreError):

    """Raise when there is a problem related to the database."""


class APIError(Exception):

    """Error thrown for API errors."""

    status_code = 400

    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert error to dict and return it."""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class UnauthorizedError(APIError):

    """Raise when there is a a lack of permissions."""

    status_code = 401
