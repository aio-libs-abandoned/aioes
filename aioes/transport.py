import asyncio
import itertools
import json
import re
import time


from .exceptions import ConnectionError, TransportError


class Transport:
    """Encapsulation of transport-related to logic.

    Handles instantiation of the individual connections as well as
    creating a connection pool to hold them.

    Main interface is the `perform_request` method.

    """

    # get ip/port from "inet[wind/127.0.0.1:9200]"
    ADDRESS_RE = re.compile(r'/(?P<host>[\.:0-9a-f]*):(?P<port>[0-9]+)\]?$')

    def __init__(self, hosts, *, sniff_timeout=0.1):
        self._hosts = hosts
        self._connection_pool
        self._seed_connections = list(self._connection_pool.connections)
        self._sniff_timeout = sniff_timeout
        self._last_sniff = time.monotonic()

    @property
    def last_sniff(self):
        return self._last_sniff

    def add_host(self, host):
        pass

    @property
    def hosts(self):
        return self._hosts

    @hosts.setter
    def hosts(self, hosts):
        self._hosts = hosts
        # TODO: reinitialize connection pool

    @asyncio.coroutine
    def get_connection(self):
        """
        Retreive a :class:`~aioes.Connection` instance from the
        :class:`~aioes.ConnectionPool` instance.
        """
        if self.sniffer_timeout:
            if time.monotonic() >= self.last_sniff + self.sniffer_timeout:
                yield from self.sniff_hosts()
        return self._connection_pool.get_connection()

    @asyncio.coroutine
    def sniff_hosts(self):
        """Obtain a list of nodes from the cluster and create a new connection
        pool using the information retrieved.

        To extract the node connection parameters use the
        `nodes_to_host_callback`.

        """
        previous_sniff = self._last_sniff
        try:
            # reset last_sniff timestamp
            self._last_sniff = time.monotonic()
            # go through all current connections as well as the
            # seed_connections for good measure
            for c in itertools.chain(self._connection_pool.connections,
                                     self._seed_connections):
                try:
                    # use small timeout for the sniffing request,
                    # should be a fast api call
                    _, headers, node_info = yield from c.perform_request(
                        'GET', '/_nodes/_all/clear',
                        timeout=self._sniff_timeout)
                    node_info = json.loads(node_info)
                    break
                except (ConnectionError, TypeError, ValueError):
                    pass
            else:
                raise TransportError("N/A", "Unable to sniff hosts.")
        except:
            # keep the previous value on error
            self._last_sniff = previous_sniff
            raise

        hosts = []
        address = Connection.transport_schema + '_address'
        for n in node_info['nodes'].values():
            match = self.ADDRESS_RE.search(n.get(address, ''))
            if not match:
                continue

            host = match.groupdict()
            if 'port' in host:
                host['port'] = int(host['port'])
            host = self.host_info_callback(n, host)
            if host is not None:
                hosts.append(host)

        # we weren't able to get any nodes, maybe using an incompatible
        # transport_schema or host_info_callback blocked all - raise error.
        if not hosts:
            raise TransportError(
                "N/A",
                "Unable to sniff hosts - no viable hosts found.")

        self.hosts = hosts

    @asyncio.coroutine
    def mark_dead(self, connection):
        """
        Mark a connection as dead (failed) in the connection pool. If sniffing
        on failure is enabled this will initiate the sniffing process.

        :arg connection: instance of :class:`~aioes.Connection` that failed
        """
        # mark as dead even when sniffing to avoid hitting this host
        # during the sniff process

        self._connection_pool.mark_dead(connection)
        if self._sniff_on_connection_fail:
            yield from self.sniff_hosts()

    @asyncio.coroutine
    def perform_request(self, method, url, params=None, body=None):
        """
        Perform the actual request. Retrieve a connection from the connection
        pool, pass all the information to it's perform_request method and
        return the data.

        If an exception was raised, mark the connection as failed and retry (up
        to `max_retries` times).

        If the operation was succesful and the connection used was previously
        marked as dead, mark it as live, resetting it's failure count.

        :arg method: HTTP method to use
        :arg url: absolute url (without host) to target
        :arg params: dictionary of query parameters, will be handed over to the
            underlying :class:`~elasticsearch.Connection` class for serialization
        :arg body: body of the request, will be serializes using serializer and
            passed to the connection
        """
        if body is not None:
            body = self.serializer.dumps(body)

            # some clients or environments don't support sending GET with body
            if method == 'GET' and self.send_get_body_as != 'GET':
                # send it as post instead
                if self.send_get_body_as == 'POST':
                    method = 'POST'

                # or as source parameter
                elif self.send_get_body_as == 'source':
                    if params is None:
                        params = {}
                    params['source'] = body
                    body = None

        if body is not None:
            try:
                body = body.encode('utf-8')
            except UnicodeDecodeError:
                # Python 2 and str, no need to re-encode
                pass

        ignore = ()
        timeout = None
        if params:
            timeout = params.pop('request_timeout', None)
            ignore = params.pop('ignore', ())
            if isinstance(ignore, int):
                ignore = (ignore, )

        for attempt in range(self.max_retries + 1):
            connection = self.get_connection()

            try:
                status, headers, data = connection.perform_request(method, url, params, body, ignore=ignore, timeout=timeout)
            except ConnectionError:
                self.mark_dead(connection)

                # raise exception on last retry
                if attempt == self.max_retries:
                    raise
            else:
                # connection didn't fail, confirm it's live status
                self.connection_pool.mark_live(connection)
                if data:
                    data = self.deserializer.loads(data, headers.get('content-type'))
                return status, data
