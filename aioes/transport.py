import asyncio
import collections
import itertools
import json
import random
import re
import time
import urllib.parse

from .connection import Connection
from .exception import ConnectionError, TransportError
from .pool import ConnectionPool

Endpoint = collections.namedtuple('TCPEndpoint', 'scheme host port')


def validate_endpoint(endpoint):
    if not isinstance(endpoint.port, int):
        raise ValueError('bad port {}'.format(endpoint.port))
    if endpoint.scheme not in ('http', 'https'):
        raise ValueError('bad scheme {}'.format(endpoint.scheme))
    if not isinstance(endpoint.host, str) or not endpoint.host:
        raise ValueError('bad host {}'.format(endpoint.host))


def get_default_port(scheme):
    return 443 if scheme == 'https' else 9200


DEFAULT_SCHEME = 'http'


class Transport:
    """Encapsulation of transport-related to logic.

    Handles instantiation of the individual connections as well as
    creating a connection pool to hold them.

    Main interface is the `perform_request` method.

    """

    # get ip/port from "inet[wind/127.0.0.1:9200]" or "127.0.0.1:9200"
    ADDRESS_RE = re.compile(
            r'(?:^|/)(?P<host>[\.:0-9a-f]*):(?P<port>[0-9]+)\]?$')

    def __init__(self, endpoints, *,
                 sniffer_interval=None, sniffer_timeout=0.1, max_retries=3,
                 loop):
        self._loop = loop
        self._endpoints = self._convert_endpoints(endpoints)
        self._pool = ConnectionPool([], loop=loop)
        self._reinitialize_endpoints()
        self._seed_connections = list(self._pool.connections)
        self._sniffer_interval = sniffer_interval
        self._sniffer_timeout = sniffer_timeout
        self._last_sniff = time.monotonic()
        self._max_retries = max_retries

    @property
    def max_retries(self):
        return self._max_retries

    @property
    def last_sniff(self):
        return self._last_sniff

    @property
    def sniffer_interval(self):
        return self._sniffer_interval

    @property
    def sniffer_timeout(self):
        return self._sniffer_timeout

    @property
    def endpoints(self):
        return list(self._endpoints)

    @endpoints.setter
    def endpoints(self, endpoints):
        self._endpoints = self._convert_endpoints(endpoints)
        self._reinitialize_endpoints()

    def close(self):
        self._pool.close()

    def _convert_endpoints(self, endpoints):
        ret = []
        for e in endpoints:
            if isinstance(e, Endpoint):
                endpoint = e
            elif isinstance(e, dict):
                try:
                    host = e['host']
                except KeyError:
                    raise RuntimeError("Bad endpoint {}".format(e))
                port = e.get('port')
                scheme = e.get('scheme', DEFAULT_SCHEME)
                if port is None:
                    port = get_default_port(scheme)
                endpoint = Endpoint(scheme, host, port)
            elif isinstance(e, str):
                if not re.match(r'^(\w*\:?)//.*', e):
                    e = '{}://{}'.format(DEFAULT_SCHEME, e)
                parts = urllib.parse.urlparse(e)
                if parts.scheme:
                    scheme = parts.scheme
                else:
                    scheme = DEFAULT_SCHEME
                try:
                    port = parts.port
                except ValueError:
                    raise RuntimeError("Bad endpoint {}".format(e))
                if port is None:
                    port = get_default_port(scheme)
                if parts.hostname:
                    auth = ':'.join(
                        [x for x in (parts.username, parts.password) if x]
                    )
                    if auth:
                        host = '{}@{}'.format(auth, parts.hostname)
                    else:
                        host = parts.hostname
                endpoint = Endpoint(scheme, host, port)
            else:
                raise RuntimeError("Bad endpoint {}".format(e))
            try:
                validate_endpoint(endpoint)
            except ValueError:
                raise RuntimeError("Bad endpoint {}".format(endpoint))
            ret.append(endpoint)
        return ret

    def _reinitialize_endpoints(self):
        old_connections = {c.endpoint: c for c in self._pool.connections}
        connections = []
        for endpoint in self._endpoints:
            if endpoint in old_connections:
                connection = old_connections[endpoint]
                connections.append(connection)
                self._pool.detach(connection)
            else:
                connections.append(Connection(endpoint, loop=self._loop))
        self._pool.close()
        random.shuffle(connections)
        self._pool = ConnectionPool(connections, loop=self._loop)

    @asyncio.coroutine
    def get_connection(self):
        """
        Retreive a :class:`~aioes.Connection` instance from the
        :class:`~aioes.ConnectionPool` instance.
        """
        if self._sniffer_interval:
            if time.monotonic() >= self._last_sniff + self._sniffer_interval:
                yield from self.sniff_endpoints()
        ret = yield from self._pool.get_connection()
        return ret

    @asyncio.coroutine
    def sniff_endpoints(self):
        """Obtain a list of nodes from the cluster and create a new connection
        pool using the information retrieved.

        To extract the node connection parameters use the
        `nodes_to_endpoint_callback`.

        """
        previous_sniff = self._last_sniff
        try:
            # reset last_sniff timestamp
            self._last_sniff = time.monotonic()
            # go through all current connections as well as the
            # seed_connections for good measure
            for c in itertools.chain(self._pool.connections,
                                     self._seed_connections):
                try:
                    # use small timeout for the sniffing request,
                    # should be a fast api call
                    _, headers, node_info = yield from asyncio.wait_for(
                        c.perform_request(
                            'GET',
                            '/_nodes/_all/clear',
                            None,
                            None),
                        timeout=self._sniffer_timeout,
                        loop=self._loop)
                except ConnectionError:
                    continue
                try:
                    node_info = json.loads(node_info)
                except (TypeError, ValueError):
                    continue
                break
            else:
                raise TransportError("N/A", "Unable to sniff endpoints.")
        except:
            # keep the previous value on error
            self._last_sniff = previous_sniff
            raise

        endpoints = []
        address = 'http_address'
        for n in node_info['nodes'].values():
            match = self.ADDRESS_RE.search(n.get(address, ''))
            if not match:
                continue

            dct = match.groupdict()
            host = dct['host']
            if 'port' in dct:
                port = int(dct['port'])
            else:
                port = 9200
            scheme = dct.get('scheme') or DEFAULT_SCHEME
            attrs = n.get('attributes', {})
            if not (attrs.get('data', 'true') == 'false' and
                    attrs.get('client', 'false') == 'false' and
                    attrs.get('master', 'true') == 'true'):
                endpoints.append(Endpoint(scheme, host, port))

        # we weren't able to get any nodes, maybe using an incompatible
        # transport_schema or host_info_callback blocked all - raise error.
        if not endpoints:
            raise TransportError(
                "N/A",
                "Unable to sniff endpoints - no viable endpoints found.")

        self.endpoints = endpoints

    @asyncio.coroutine
    def _mark_dead(self, connection):
        """
        Mark a connection as dead (failed) in the connection pool. If sniffing
        on failure is enabled this will initiate the sniffing process.

        :arg connection: instance of :class:`~aioes.Connection` that failed
        """
        # mark as dead even when sniffing to avoid hitting this endpoint
        # during the sniff process

        yield from self._pool.mark_dead(connection)
        yield from self.sniff_endpoints()

    @asyncio.coroutine
    def perform_request(self, method, url, params=None, body=None,
                        *, request_timeout=None, decoder=json.loads):
        """
        Perform the actual request. Retrieve a connection from the connection
        pool, pass all the information to it's perform_request method and
        return the data.

        If an exception was raised, mark the connection as failed and retry (up
        to `max_retries` times).

        If the operation was succesful and the connection used was previously
        marked as dead, mark it as live, resetting it's failure count.

        :arg method: HTTP method to use
        :arg url: absolute url (without endpoint) to target
        :arg params: dictionary of query parameters, will be handed over to the
          underlying :class:`~elasticsearch.Connection` class for serialization
        :arg body: body of the request, will be serializes using serializer and
            passed to the connection
        """
        if body is not None:
            if not isinstance(body, (str, bytes)):
                body = json.dumps(body)
            body = body.encode('utf-8')

        for attempt in range(self.max_retries + 1):
            connection = yield from self.get_connection()

            try:
                status, headers, data = yield from asyncio.wait_for(
                    connection.perform_request(
                        method,
                        url,
                        params,
                        body),
                    request_timeout,
                    loop=self._loop)
            except ConnectionError:
                yield from self._mark_dead(connection)

                # raise exception on last retry
                if attempt == self.max_retries:
                    raise
            else:
                # connection didn't fail, confirm it's live status
                yield from self._pool.mark_live(connection)
                if data:
                    data = decoder(data)
                return status, data
