import asyncio

from .utils import NamespacedClient
from .utils import _make_path

default = object()


class IndicesClient(NamespacedClient):

    @asyncio.coroutine
    def analyze(self, index=None, body=None, *,
                analyzer=default, char_filters=default, field=default,
                filters=default, prefer_local=default, text=default,
                tokenizer=default, pretty=default, format=default):
        """
        Perform the analysis process on a text and return the tokens breakdown of the text.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-analyze.html>`_

        :arg index: The name of the index to scope the operation
        :arg body: The text on which the analysis should be performed
        :arg analyzer: The name of the analyzer to use
        :arg char_filters: A comma-separated list of character filters to use
            for the analysis
        :arg field: Use the analyzer configured for this field (instead of
            passing the analyzer name)
        :arg filters: A comma-separated list of filters to use for the analysis
        :arg format: Format of the output, default u'detailed'
        :arg index: The name of the index to scope the operation
        :arg prefer_local: With `true`, specify that a local shard should be
            used if available, with `false`, use a random shard (default: true)
        :arg text: The text on which the analysis should be performed (when
            request body is not used)
        :arg tokenizer: The name of the tokenizer to use for the analysis
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
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

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
               master_timeout=default, pretty=default, format=default):
        """
        Create an index in Elasticsearch.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-create-index.html>`_

        :arg index: The name of the index
        :arg body: The configuration for the index (`settings` and `mappings`)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self.transport.perform_request(
            'PUT',
            _make_path(index),
            params=params,
            body=body)
        return data

    @asyncio.coroutine
    def open(self, index, *, timeout=default, master_timeout=default,
             allow_no_indices=default, expand_wildcards=default,
             ignore_unavailable=default, pretty=default, format=default):
        """
        Open a closed index to make it available for search.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-open-close.html>`_

        :arg index: The name of the index
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all` string or
            when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :arg ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
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
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, '_open'),
            params=params)
        return data

    @asyncio.coroutine
    def close(self, index, *, allow_no_indices=default,
              expand_wildcards=default, ignore_unavailable=default,
              master_timeout=default, timeout=default, pretty=default,
              format=default):
        """
        Close an index to remove it's overhead from the cluster. Closed index
        is blocked for read/write operations.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-open-close.html>`_

        :arg index: A comma-separated list of indices to close; use `_all` or
            '*' to close all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default u'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
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
        if pretty is not default:
            params['pretty'] = pretty
        if format is not default:
            params['format'] = format

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, '_close'),
            params=params)
        return data

    def delete(self):
        pass

    def exists(self):
        pass

    def exists_type(self):
        pass

    def put_mapping(self):
        pass

    def get_mapping(self):
        pass

    def get_field_mapping(self):
        pass

    def delete_mapping(self):
        pass

    def put_alias(self):
        pass

    def exists_alias(self):
        pass

    def get_alias(self):
        pass

    def get_aliases(self):
        pass

    def update_aliases(self):
        pass

    def delete_alias(self):
        pass

    def put_template(self):
        pass

    def exists_template(self):
        pass

    def get_template(self):
        pass

    def delete_template(self):
        pass

    def get_settings(self):
        pass

    def put_settings(self):
        pass

    def put_warmer(self):
        pass

    def get_warmer(self):
        pass

    def delete_warmer(self):
        pass

    def status(self):
        pass

    def stats(self):
        pass

    def segments(self):
        pass

    def optimize(self):
        pass

    def validate_query(self):
        pass

    def clear_cache(self):
        pass

    def recovery(self):
        pass

    def snapshot_index(self):
        pass
