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
            self._sniff_hosts()
