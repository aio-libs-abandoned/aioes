from datetime import date, datetime
from urllib.parse import quote_plus

# parts of URL to be omitted
SKIP_IN_PATH = (None, b'', [], ())


def _escape(value):
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # make sequences into comma-separated stings
    if isinstance(value, (list, tuple)):
        value = ','.join(value)

    # dates and datetimes into isoformat
    elif isinstance(value, (date, datetime)):
        value = value.isoformat()

    # make bools into true/false strings
    elif isinstance(value, bool):
        value = str(value).lower()

    # encode strings to utf-8
    if isinstance(value, (str, bytes)):
        try:
            return value.encode('utf-8')
        except UnicodeDecodeError:
            # Python 2 and str, no need to re-encode
            pass

    return str(value)


def _make_path(*parts):
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists and tuples to comma separated values.
    """
    # TODO: maybe only allow some parts to be lists/tuples ?
    # preserve ',' and '*' in url for nicer URLs in logs
    return '/' + '/'.join(
        quote_plus(_escape(p), b',*')
        for p in parts if p not in SKIP_IN_PATH)


class NamespacedClient:

    def __init__(self, client):
        self._client = client

    @property
    def client(self):
        return self._client

    @property
    def transport(self):
        return self._client.transport
