import asyncio
import json
import logging

import aiohttp
from .exception import HTTP_EXCEPTIONS, TransportError

logger = logging.getLogger(__name__)


class Connection:
    """
    Class responsible for maintaining a connection to an Elasticsearch node.
    Holds persistent connection pool to it.

    Also responsible for logging.
    """

    def __init__(self, endpoint, *, loop):
        self._loop = loop
        self._endpoint = endpoint
        self._connector = aiohttp.TCPConnector(resolve=True)
        self._base_url = 'http://{0[0]}:{0[1]}/'.format(endpoint)

    @property
    def endpoint(self):
        return self._endpoint

    def close(self):
        self._connector.close()

    @asyncio.coroutine
    def perform_request(self, method, url, params, body):
        url = self._base_url + url
        resp = yield from aiohttp.request(method, url, params, body)
        resp_body = yield from resp.text()
        if not (200 <= resp.status <= 300):
            extra = None
            try:
                extra = json.loads(resp_body)
            except ValueError:
                pass
            exc_class = HTTP_EXCEPTIONS.get(resp.status, TransportError)
            raise exc_class(resp.status, resp_body, extra)
        return resp.status, resp.headers, resp_body
