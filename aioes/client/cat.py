import asyncio

from .utils import NamespacedClient
from .utils import _make_path

default = object()


def _decode_text(s):
    return s


class CatClient(NamespacedClient):

    @asyncio.coroutine
    def aliases(self, *, name=default, h=default, help=default,
                local=default, master_timeout=default, v=default):
        """
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cat-alias.html>`_

        :arg name: A comma-separated list of alias names to return
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to
            master node
        :arg v: Verbose mode. Display column headers, default False
        """
        params = {}
        if name is not default:
            params['name'] = name
        if h is not default:
            params['h'] = h
        if help is not default:
            params['help'] = bool(help)
        if local is not default:
            params['local'] = bool(local)
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if v is not default:
            params['v'] = bool(v)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path('_cat', 'aliases', name),
            params=params, decoder=_decode_text
        )
        return data

    @asyncio.coroutine
    def allocation(self, node_id=None, *,
                   h=default, help=default, local=default,
                   master_timeout=default, v=default):
        """
        Allocation provides a snapshot of how shards have located around the
        cluster and the state of disk usage.

        """
        params = {}
        if h is not default:
            params['h'] = h
        if help is not default:
            params['help'] = bool(help)
        if local is not default:
            params['local'] = bool(local)
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if v is not default:
            params['v'] = bool(v)
        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path('_cat', 'allocation', node_id),
            params=params, decoder=_decode_text)
        return data

    @asyncio.coroutine
    def help(self, *, help=default):
        """A simple help for the cat api."""
        params = {}
        if help is not default:
            params['help'] = bool(help)
        _, data = yield from self.transport.perform_request(
            'GET', '/_cat', params=params, decoder=_decode_text)
        return data
