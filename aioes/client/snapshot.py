import asyncio

from .utils import NamespacedClient
from .utils import _make_path

default = object()


class SnapshotClient(NamespacedClient):

    @asyncio.coroutine
    def create(self, repository, snapshot, body=None, *,
               master_timeout=default, wait_for_completion=default):
        """
        Create a snapshot in repository
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A snapshot name
        :arg body: The snapshot definition
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg wait_for_completion: Should this request wait until
            the operation has completed before returning, default False
        """
        params = {}

        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if wait_for_completion is not default:
            params['wait_for_completion'] = bool(wait_for_completion)

        _, data = yield from self.transport.perform_request(
            'PUT', _make_path('_snapshot', repository, snapshot),
            params=params, body=body
        )
        return data

    @asyncio.coroutine
    def delete(self, repository, snapshot, *, master_timeout=default):
        """
        Deletes a snapshot from a repository.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A snapshot name
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        params = {}

        if master_timeout is not default:
            params['master_timeout'] = master_timeout

        _, data = yield from self.transport.perform_request(
            'DELETE',
            _make_path('_snapshot', repository, snapshot),
            params=params
        )
        return data

    @asyncio.coroutine
    def get(self, repository, snapshot, *, master_timeout=default):
        """
        Retrieve information about a snapshot.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A comma-separated list of repository names
        :arg snapshot: A comma-separated list of snapshot names
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        params = {}

        if master_timeout is not default:
            params['master_timeout'] = master_timeout

        _, data = yield from self.transport.perform_request(
            'GET', _make_path('_snapshot', repository, snapshot),
            params=params
        )
        return data

    @asyncio.coroutine
    def delete_repository(self, repository, *, master_timeout=default,
                          timeout=default):
        """
        Removes a shared file system repository.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A comma-separated list of repository names
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        params = {}

        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if timeout is not default:
            params['timeout'] = timeout

        _, data = yield from self.transport.perform_request(
            'DELETE',
            _make_path('_snapshot', repository),
            params=params
        )
        return data

    @asyncio.coroutine
    def get_repository(self, repository=None, *, local=default,
                       master_timeout=default):
        """
        Return information about registered repositories.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A comma-separated list of repository names
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
        params = {}

        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if local is not default:
            params['local'] = bool(local)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path('_snapshot', repository),
            params=params
        )
        return data

    @asyncio.coroutine
    def create_repository(self, repository, body, *, master_timeout=default,
                          timeout=default):
        """
        Registers a shared file system repository.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg body: The repository definition
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        params = {}

        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if timeout is not default:
            params['timeout'] = timeout

        _, data = yield from self.transport.perform_request(
            'PUT', _make_path('_snapshot', repository),
            params=params, body=body
        )
        return data

    @asyncio.coroutine
    def restore(self, repository, snapshot, body=None, *,
                master_timeout=default, wait_for_completion=default):
        """
        Restore a snapshot.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A snapshot name
        :arg body: Details of what to restore
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg wait_for_completion: Should this request wait until the operation
            has completed before returning, default False
        """
        params = {}

        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if wait_for_completion is not default:
            params['wait_for_completion'] = bool(wait_for_completion)

        _, data = yield from self.transport.perform_request(
            'POST', _make_path('_snapshot', repository, snapshot, '_restore'),
            params=params, body=body
        )
        return data

    @asyncio.coroutine
    def status(self, repository=None, snapshot=None, *,
               master_timeout=default):
        """Get snapshot status

        :arg repository: A repository name
        :arg snapshot: A comma-separated list of snapshot names
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        params = {}
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path('_snapshot', repository, snapshot, '_status'),
            params=params)
        return data
