__all__ = [
    'ElasticsearchException',
    'TransportError', 'NotFoundError', 'ConflictError',
    'RequestError', 'ConnectionError'
]


class ElasticsearchException(Exception):
    """Base elastic search exception.

    Base class for all exceptions raised by this package's operations.
    """


class SerializationError(ElasticsearchException):
    """
    Data passed in failed to serialize properly in the ``Serializer`` being
    used.
    """


class TransportError(ElasticsearchException):
    """Transport error.

    Exception raised when ES returns a non-OK (>=400) HTTP status
    code. Or when an actual connection error happens; in that case the
    ``status_code`` will be set to ``'N/A'``.
    """
    @property
    def status_code(self):
        """
        The HTTP status code of the response that precipitated the error or
        ``'N/A'`` if not applicable.
        """
        return self.args[0]

    @property
    def error(self):
        """A string error message."""
        return self.args[1]

    @property
    def info(self):
        """Dict of returned error info from ES, where available."""
        return self.args[2]

    def __str__(self):
        return 'TransportError(%s, %r)' % (self.status_code, self.error)


class ConnectionError(TransportError):
    """Connection error.

    Error raised when there was an exception while talking to
    ES. Original exception from the underlying Connection
    implementation is available as .info.
    """
    def __str__(self):
        return 'ConnectionError(%s) caused by: %s(%s)' % (
            self.error, self.info.__class__.__name__, self.info)


class NotFoundError(TransportError):
    """Exception representing a 404 status code."""


class ConflictError(TransportError):
    """Exception representing a 409 status code."""


class RequestError(TransportError):
    """Exception representing a 400 status code."""

# more generic mappings from status_code to python exceptions
HTTP_EXCEPTIONS = {
    400: RequestError,
    404: NotFoundError,
    409: ConflictError,
}
