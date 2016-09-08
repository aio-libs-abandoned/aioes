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

    def __init__(self, endpoint, *, loop, verify_ssl=True):
        self._endpoint = endpoint
        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                use_dns_cache=True,
                loop=loop,
                verify_ssl=verify_ssl),
            loop=loop)
        self._base_url = '{0.scheme}://{0.host}:{0.port}/'.format(endpoint)

    @property
    def endpoint(self):
        return self._endpoint

    def close(self):
        return self._session.close()

    @asyncio.coroutine
    def perform_request(self, method, url, params, body):
        url = self._base_url + url
        resp = yield from self._session.request(
            method, url, params=params, data=body)
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
