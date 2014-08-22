import asyncio

from .utils import NamespacedClient
from .utils import _make_path

default = object()


class IndicesClient(NamespacedClient):

    @asyncio.coroutine
    def analyze(self, index=None, body=None, *,
                analyzer=default, char_filters=default, field=default,
                filters=default, prefer_local=default, text=default,
                tokenizer=default, token_filters=default):
        """
        Perform the analysis process on a text and return the tokens breakdown
        of the text.
        """
        params = {}
        if analyzer is not default:
            params['analyzer'] = analyzer
        if char_filters is not default:
            params['char_filters'] = char_filters
        if field is not default:
            params['field'] = field
        if filters is not default:
            params['filters'] = filters
        if prefer_local is not default:
            params['prefer_local'] = prefer_local
        if text is not default:
            params['text'] = text
        if tokenizer is not default:
            params['tokenizer'] = tokenizer
        if token_filters is not default:
            params['token_filters'] = token_filters

        _, data = yield from self.transport.perform_request(
            'GET',
            _make_path(index, '_analyze'),
            params=params, body=body)
        return data

    def refresh(self):
        pass

    def flush(self):
        pass

    @asyncio.coroutine
    def create(self, index, body=None, *, timeout=default,
               master_timeout=default):
        """
        Create an index in Elasticsearch.
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = master_timeout

        _, data = yield from self.transport.perform_request(
            'PUT',
            _make_path(index),
            params=params,
            body=body)
        return data

    @asyncio.coroutine
    def open(self, index, *, timeout=default, master_timeout=default,
             allow_no_indices=default, expand_wildcards=default,
             ignore_unavailable=default):
        """
        Open a closed index to make it available for search.
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['allow_no_indices'] = allow_no_indices
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, '_open'),
            params=params)
        return data

    @asyncio.coroutine
    def close(self, index, *, allow_no_indices=default,
              expand_wildcards=default, ignore_unavailable=default,
              master_timeout=default, timeout=default):
        """
        Close an index to remove it's overhead from the cluster. Closed index
        is blocked for read/write operations.
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if allow_no_indices is not default:
            params['allow_no_indices'] = allow_no_indices
        if expand_wildcards is not default:
            params['allow_no_indices'] = allow_no_indices
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = ignore_unavailable

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, '_close'),
            params=params)
        return data

    @asyncio.coroutine
    def delete(self):
        pass

    @asyncio.coroutine
    def exists(self):
        pass

    @asyncio.coroutine
    def exists_type(self):
        pass

    @asyncio.coroutine
    def put_mapping(self):
        pass

    @asyncio.coroutine
    def get_mapping(self):
        pass

    @asyncio.coroutine
    def get_field_mapping(self):
        pass

    @asyncio.coroutine
    def delete_mapping(self):
        pass

    @asyncio.coroutine
    def put_alias(self):
        pass

    @asyncio.coroutine
    def exists_alias(self):
        pass

    @asyncio.coroutine
    def get_alias(self):
        pass

    @asyncio.coroutine
    def get_aliases(self):
        pass

    @asyncio.coroutine
    def update_aliases(self):
        pass

    @asyncio.coroutine
    def delete_alias(self):
        pass

    @asyncio.coroutine
    def put_template(self):
        pass

    @asyncio.coroutine
    def exists_template(self):
        pass

    @asyncio.coroutine
    def get_template(self):
        pass

    @asyncio.coroutine
    def delete_template(self):
        pass

    @asyncio.coroutine
    def get_settings(self):
        pass

    @asyncio.coroutine
    def put_settings(self):
        pass

    @asyncio.coroutine
    def put_warmer(self):
        pass

    @asyncio.coroutine
    def get_warmer(self):
        pass

    @asyncio.coroutine
    def delete_warmer(self):
        pass

    @asyncio.coroutine
    def status(self):
        pass

    @asyncio.coroutine
    def stats(self):
        pass

    @asyncio.coroutine
    def segments(self):
        pass

    @asyncio.coroutine
    def optimize(self):
        pass

    @asyncio.coroutine
    def validate_query(self):
        pass

    @asyncio.coroutine
    def clear_cache(self):
        pass

    @asyncio.coroutine
    def recovery(self):
        pass

    @asyncio.coroutine
    def snapshot_index(self):
        pass
