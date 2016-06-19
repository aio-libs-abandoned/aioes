import abc
import asyncio
import collections
import random
import time

from .log import logger


class AbstractSelector(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def select(self, connections):
        pass  # pragma: no cover


class RandomSelector(AbstractSelector):

    def select(self, connections):
        return random.choice(connections)


class RoundRobinSelector(AbstractSelector):
    def __init__(self):
        self._current = 0

    def select(self, connections):
        self._current += 1
        if self._current >= len(connections):
            self._current = 0
        return connections[self._current]


class ConnectionPool:
    def __init__(self, connections, *, dead_timeout=60, timeout_cutoff=5,
                 selector_factory=RoundRobinSelector,
                 loop):
        self._dead_timeout = dead_timeout
        self._timeout_cutoff = timeout_cutoff
        self._selector = selector_factory()
        self._dead = asyncio.PriorityQueue(len(connections), loop=loop)
        self._dead_count = collections.Counter()
        self._connections = connections

    def close(self):
        for connection in self._connections:
            connection.close()

    def detach(self, connection):
        self._connections.remove(connection)

    @property
    def connections(self):
        return list(self._connections)

    @property
    def dead_timeout(self):
        return self._dead_timeout

    @property
    def timeout_cutoff(self):
        return self._timeout_cutoff

    @asyncio.coroutine
    def mark_dead(self, connection):
        """
        Mark the connection as dead (failed). Remove it from the live pool and
        put it on a timeout.

        :arg connection: the failed instance
        """
        now = time.monotonic()
        try:
            self._connections.remove(connection)
        except ValueError:
            # connection not alive or another thread marked it already, ignore
            return
        else:
            self._dead_count[connection] += 1
            dead_count = self._dead_count[connection]
            timeout = self._dead_timeout * 2 ** min(dead_count - 1,
                                                    self._timeout_cutoff)
            yield from self._dead.put((now + timeout, connection))
            logger.warning(
                "Connection %r has failed for %i times in a row, "
                "putting on %i second timeout.",
                connection, dead_count, timeout
            )

    @asyncio.coroutine
    def mark_live(self, connection):
        """
        Mark connection as healthy after a resurrection. Resets the fail
        counter for the connection.

        :arg connection: the connection to redeem
        """
        del self._dead_count[connection]

    @asyncio.coroutine
    def resurrect(self, force=False):
        """
        Attempt to resurrect a connection from the dead pool. It will try to
        locate one (not all) eligible (it's timeout is over) connection to
        return to th live pool.

        :arg force: resurrect a connection even if there is none eligible (used
            when we have no live connections)
        """
        if self._dead.empty():
            return

        timeout, connection = self._dead.get_nowait()

        if not force and timeout > time.monotonic():
            # return it back if not eligible and not forced
            yield from self._dead.put((timeout, connection))
            return

        # either we were forced or the connection is elligible to be retried
        self._connections.append(connection)
        logger.info('Resurrecting connection %r (force=%s).',
                    connection, force)

    @asyncio.coroutine
    def get_connection(self):
        """
        Return a connection from the pool using the `ConnectionSelector`
        instance.

        It tries to resurrect eligible connections, forces a resurrection when
        no connections are availible and passes the list of live connections to
        the selector instance to choose from.

        Returns a connection instance
        """
        yield from self.resurrect()

        # no live nodes, resurrect one by force
        if not self._connections:
            yield from self.resurrect(True)

        connection = self._selector.select(self._connections)

        return connection
