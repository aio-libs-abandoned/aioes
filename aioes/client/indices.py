import asyncio

from .utils import NamespacedClient
from .utils import _make_path
from aioes.exception import NotFoundError

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

    @asyncio.coroutine
    def refresh(self, index=None, *,
                allow_no_indices=default, expand_wildcards=default,
                ignore_indices=default, ignore_unavailable=default,
                force=default):
        """
        Explicitly refresh one or more index, making all operations performed
        since the last refresh available for search.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-refresh.html>`_

        :param index: A comma-separated list of index names; use `_all` or
               empty string to perform the operation on all indices
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows to
               ignore `missing` ones, default u'none'
        :param ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
        :param force: Force a refresh even if not required
        """
        params = {}
        if force is not default:
            params['force'] = bool(force)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_indices is not default:
            params['ignore_indices'] = ignore_indices
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, '_refresh'),
            params=params)
        return data

    @asyncio.coroutine
    def flush(self, index=None, *,
              force=default, full=default, allow_no_indices=default,
              expand_wildcards=default, ignore_indices=default,
              ignore_unavailable=default):
        """
        Explicitly flush one or more indices.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-flush.html>`_

        :param index: A comma-separated list of index names; use `_all` or
               empty string for all indices
        :param force: Whether a flush should be forced even if it is not
               necessarily needed ie. if no changes will be committed to
               the index.
        :param full: If set to true a new index writer is created and settings
               that have been changed related to the index writer will be
               refreshed.
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows to
               ignore `missing` ones (default: none)
        :param ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
        """
        params = {}
        if force is not default:
            params['force'] = bool(force)
        if full is not default:
            params['full'] = bool(full)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_indices is not default:
            params['ignore_indices'] = ignore_indices
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, '_flush'),
            params=params)
        return data

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
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)

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
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, '_close'),
            params=params)
        return data

    @asyncio.coroutine
    def delete(self, index, *,
               timeout=default, master_timeout=default):
        """
        Delete an index in Elasticsearch
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-delete-index.html>`_

        :param index: A comma-separated list of indices to delete; use `_all`
               or '*' to delete all indices
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = master_timeout

        _, data = yield from self.transport.perform_request(
            'DELETE',
            _make_path(index),
            params=params)
        return data

    @asyncio.coroutine
    def exists(self, index, *,
               allow_no_indices=default, expand_wildcards=default,
               ignore_unavailable=default, local=default):
        """
        Return a boolean indicating whether given index exists.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-indices-exists.html>`_

        :param index: A list of indices to check
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both., default u'open'
        :param ignore_unavailable: Whether specified concrete indices should be
               ignored when unavailable (missing or closed)
        :param local: Return local information, do not retrieve the state from
               master node (default: false)
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if local is not default:
            params['local'] = bool(local)

        try:
            yield from self.transport.perform_request(
                'HEAD', _make_path(index), params=params)
        except NotFoundError:
            return False
        return True

    @asyncio.coroutine
    def exists_type(self, index, doc_type, *,
                    allow_no_indices=default, expand_wildcards=default,
                    ignore_indices=default, ignore_unavailable=default,
                    local=default):
        """
        Check if a type/types exists in an index/indices.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-types-exists.html>`_

        :param index: A comma-separated list of index names; use `_all` to
               check the types across all indices
        :param doc_type: A comma-separated list of document types to check
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows to
               ignore `missing` ones (default: none)
        :param ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
        :param local: Return local information, do not retrieve the state from
               master node (default: false)
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if ignore_indices is not default:
            params['ignore_indices'] = ignore_indices
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if local is not default:
            params['local'] = bool(local)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        try:
            yield from self.transport.perform_request(
                'HEAD', _make_path(index, doc_type), params=params)
        except NotFoundError:
            return False
        return True

    # @asyncio.coroutine
    # def put_mapping(self):
    #     pass
    #
    # @asyncio.coroutine
    # def get_mapping(self):
    #     pass
    #
    # @asyncio.coroutine
    # def get_field_mapping(self):
    #     pass
    #
    # @asyncio.coroutine
    # def delete_mapping(self):
    #     pass
    #
    # @asyncio.coroutine
    # def put_alias(self):
    #     pass
    #
    # @asyncio.coroutine
    # def exists_alias(self):
    #     pass
    #
    # @asyncio.coroutine
    # def get_alias(self):
    #     pass
    #
    # @asyncio.coroutine
    # def get_aliases(self):
    #     pass
    #
    # @asyncio.coroutine
    # def update_aliases(self):
    #     pass
    #
    # @asyncio.coroutine
    # def delete_alias(self):
    #     pass
    #
    # @asyncio.coroutine
    # def put_template(self):
    #     pass
    #
    # @asyncio.coroutine
    # def exists_template(self):
    #     pass
    #
    # @asyncio.coroutine
    # def get_template(self):
    #     pass
    #
    # @asyncio.coroutine
    # def delete_template(self):
    #     pass

    @asyncio.coroutine
    def get_settings(self, index=None, name=None, *,
                     expand_wildcards=default, ignore_indices=default,
                     ignore_unavailable=default, flat_settings=default,
                     local=default):
        """
        Retrieve settings for one or more (or all) indices.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-get-settings.html>`_

        :param index: A comma-separated list of index names; use `_all` or
               empty string to perform the operation on all indices
        :param name: The name of the settings that should be included
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows to
               ignore `missing` ones, default u'none'
        :param ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
        :param flat_settings: Return settings in flat format (default: false)
        :param local: Return local information, do not retrieve the state from
               master node (default: false)
        """
        params = {}
        if ignore_indices is not default:
            params['ignore_indices'] = str(ignore_indices)
        if flat_settings is not default:
            params['flat_settings'] = bool(flat_settings)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if local is not default:
            params['local'] = bool(local)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_settings', name),
            params=params)
        return data

    @asyncio.coroutine
    def put_settings(self, body, index=None, *,
                     allow_no_indices=default, expand_wildcards=default,
                     flat_settings=default, ignore_unavailable=default,
                     master_timeout=default):
        """
        Change specific index level settings in real time.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-update-settings.html>`_

        :param body: The index settings to be updated
        :param index: A comma-separated list of index names; use `_all` or
               empty string to perform the operation on all indices
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both., default
               u'open'
        :param flat_settings: Return settings in flat format (default: false)
        :param ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
        :param master_timeout: Specify timeout for connection to master
        """
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if flat_settings is not default:
            params['flat_settings'] = bool(flat_settings)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if master_timeout is not default:
            params['master_timeout'] = master_timeout

        _, data = yield from self.transport.perform_request(
            'PUT', _make_path(index, '_settings'),
            params=params, body=body)
        return data

    # @asyncio.coroutine
    # def put_warmer(self):
    #     pass
    #
    # @asyncio.coroutine
    # def get_warmer(self):
    #     pass
    #
    # @asyncio.coroutine
    # def delete_warmer(self):
    #     pass
    #
    @asyncio.coroutine
    def status(self, index=None, *,
               allow_no_indices=default, expand_wildcards=default,
               ignore_indices=default, ignore_unavailable=default,
               operation_threading=default, recovery=default, snapshot=default,
               human=default):
        """
        Get a comprehensive status information of one or more indices.
        `<http://elasticsearch.org/guide/reference/api/admin-indices-_/>`_

        :param index: A comma-separated list of index names; use `_all` or
               empty string to perform the operation on all indices
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows
               to ignore `missing` ones, default u'none'
        :param ignore_unavailable: Whether specified concrete indices
               should be ignored when unavailable (missing or closed)
        :param operation_threading: TODO: ?
        :param recovery: Return information about shard recovery
        :param snapshot: For snapshot status set it to true
        :param human: Whether to return time and byte values in human-readable
               format.
        """
        params = {}
        if ignore_indices is not default:
            params['ignore_indices'] = ignore_indices
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if recovery is not default:
            params['recovery'] = bool(recovery)
        if snapshot is not default:
            params['snapshot'] = bool(snapshot)
        if operation_threading is not default:
            params['operation_threading'] = operation_threading
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if human is not default:
            params['human'] = bool(human)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_status'),
            params=params)
        return data

    @asyncio.coroutine
    def stats(self, index=None, *, metric=default,
              completion_fields=default, docs=default,
              fielddata_fields=default, fields=default,
              groups=default, allow_no_indices=default,
              expand_wildcards=default, ignore_indices=default,
              ignore_unavailable=default, human=default, level=default,
              types=default):
        """
        Retrieve statistics on different operations happening on an index.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-stats.html>`_
        :param index: A comma-separated list of index names; use `_all` or
               empty string to perform the operation on all indices
        :param metric: A comma-separated list of metrics to display. Possible
               values: "_all", "completion", "docs", "fielddata",
               "filter_cache", "flush", "get", "id_cache", "indexing", "merge",
               "percolate", "refresh", "search", "segments", "store", "warmer"
        :param completion_fields: A comma-separated list of fields for
               `completion` metric (supports wildcards)
        :param docs: the number of docs / deleted docs (docs not yet merged
               out). Note, affected by refreshing the index
        :param fielddata_fields: A comma-separated list of fields for
               `fielddata` metric (supports wildcards)
        :param fields: A comma-separated list of fields for `fielddata` and
               `completion` metric (supports wildcards)
        :param groups: A comma-separated list of search groups for `search`
               statistics
        :param allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows
               to ignore `missing` ones (default: none)
        :param ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
        :param human: Whether to return time and byte values in human-readable
               format.
        :param level: Return stats aggregated at cluster, index or shard level.
               ("cluster", "indices" or "shards", default: "indices")
        :param types: A comma-separated list of document types for the
               `indexing` index metric
        """
        params = {}
        if completion_fields is not default:
            params['completion_fields'] = completion_fields
        if docs is not default:
            params['docs'] = docs
        if types is not default:
            params['types'] = types
        if fielddata_fields is not default:
            params['fielddata_fields'] = fielddata_fields
        if fields is not default:
            params['fields'] = fields
        if groups is not default:
            params['groups'] = groups

        if ignore_indices is not default:
            params['ignore_indices'] = ignore_indices
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if human is not default:
            params['human'] = bool(human)
        if level is not default:
            if not isinstance(level, str):
                raise TypeError("'level' parameter is not a string")
            elif level.lower() in ('cluster', 'indices', 'shards'):
                params['level'] = level.lower()
            else:
                raise ValueError("'level' parameter should be one"
                                 " of 'cluster', 'indices', 'shards'")
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if metric is not default:
            if not isinstance(metric, str):
                raise TypeError("'metric' parameter is not a string")
            elif metric.lower() in ('_all', 'completion', 'docs', 'fielddata',
                                    'filter_cache', 'flush', 'get', 'id_cache',
                                    'indexing', 'merge', 'percolate',
                                    'refresh', 'search', 'segments', 'store',
                                    'warmer'):
                params['metric'] = metric.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of '_all', 'completion', 'docs', "
                                 "'fielddata', 'filter_cache', 'flush', "
                                 "'get', 'id_cache', 'indexing', 'merge', "
                                 "'percolate', 'refresh', 'search', "
                                 "'segments', 'store', 'warmer'")

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_stats', metric),
            params=params)
        return data

    @asyncio.coroutine
    def segments(self, index=None, *,
                 allow_no_indices=default, expand_wildcards=default,
                 ignore_indices=default, ignore_unavailable=default,
                 human=default):
        """
        Provide low level segments information that a Lucene index (shard
        level) is built with.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-segments.html>`_

        :param index: A comma-separated list of index names; use `_all` or
               empty string to perform the operation on all indices
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows to
               ignore `missing` ones, default u'none'
        :param ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
        :param human: Whether to return time and byte values in human-readable
               format (default: false)
        """
        params = {}
        if ignore_indices is not default:
            params['ignore_indices'] = ignore_indices
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if human is not default:
            params['human'] = bool(human)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_segments'), params=params)
        return data

    @asyncio.coroutine
    def optimize(self, index=None, *,
                 flush=default, allow_no_indices=default,
                 expand_wildcards=default, ignore_indices=default,
                 ignore_unavailable=default, max_num_segments=default,
                 only_expunge_deletes=default, operation_threading=default,
                 wait_for_merge=default, force=default):
        """
        Explicitly optimize one or more indices through an API.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-optimize.html>`_

        :param index: A comma-separated list of index names; use `_all` or
               empty string to perform the operation on all indices
        :param flush: Specify whether the index should be flushed after
            performing the operation (default: true)
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows to
               ignore `missing` ones, default u'none'
        :param ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
        :param max_num_segments: The number of segments the index should be
               merged into (default: dynamic)
        :param only_expunge_deletes: Specify whether the operation should only
               expunge deleted documents
        :param operation_threading: TODO: ?
        :param wait_for_merge: Specify whether the request should block until
               the merge process is finished (default: true)
        """
        params = {}
        if force is not default:
            params['force'] = bool(force)
        if flush is not default:
            params['flush'] = bool(flush)
        if max_num_segments is not default:
            params['max_num_segments'] = int(max_num_segments)
        if ignore_indices is not default:
            params['ignore_indices'] = ignore_indices
        if only_expunge_deletes is not default:
            params['only_expunge_deletes'] = bool(only_expunge_deletes)
        if operation_threading is not default:
            params['operation_threading'] = operation_threading
        if wait_for_merge is not default:
            params['wait_for_merge'] = bool(wait_for_merge)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)

        _, data = yield from self.transport.perform_request(
            'POST', _make_path(index, '_optimize'), params=params)
        return data

    @asyncio.coroutine
    def validate_query(self, index=None, doc_type=None, body=None, *,
                       explain=default, allow_no_indices=default,
                       expand_wildcards=default, ignore_indices=default,
                       ignore_unavailable=default, operation_threading=default,
                       q=default, source=default):
        """
        Validate a potentially expensive query without executing it.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/search-validate.html>`_

        :param index: A comma-separated list of index names to restrict the
               operation; use `_all` or empty string to perform the operation
               on all indices
        :param doc_type: A comma-separated list of document types to restrict
               the operation; leave empty to perform the operation on all types
        :param body: The query definition
        :param explain: Return detailed information about the error
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows to
               ignore `missing` ones (default: none)
        :param ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
        :param operation_threading: TODO: ?
        :param q: Query in the Lucene query string syntax
        :param source: The URL-encoded query definition (instead of using the
               request body)
        """
        params = {}
        if explain is not default:
            params['explain'] = bool(explain)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if q is not default:
            params['q'] = str(q)
        if ignore_indices is not default:
            params['ignore_indices'] = ignore_indices
        if source is not default:
            params['source'] = str(source)
        if operation_threading is not default:
            params['operation_threading'] = operation_threading
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, doc_type, '_validate', 'query'),
            params=params, body=body)
        return data

    @asyncio.coroutine
    def clear_cache(self, index=None, *,
                    field_data=default, fielddata=default, fields=default,
                    filter=default, filter_cache=default, filter_keys=default,
                    id=default, id_cache=default, allow_no_indices=default,
                    expand_wildcards=default, ignore_indices=default,
                    ignore_unavailable=default, recycler=default):
        """
        Clear either all caches or specific cached associated with one or
        more indices.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/current/indices-clearcache.html>`_

        :param index: A comma-separated list of index name to limit the
               operation
        :param field_data: Clear field data
        :param fielddata: Clear field data
        :param fields: A comma-separated list of fields to clear when using
               the `field_data` parameter (default: all)
        :param filter: Clear filter caches
        :param filter_cache: Clear filter caches
        :param filter_keys: A comma-separated list of keys to clear when using
               the `filter_cache` parameter (default: all)
        :param id: Clear ID caches for parent/child
        :param id_cache: Clear ID caches for parent/child
        :param allow_no_indices: Whether to ignore if a wildcard indices
               expression resolves into no concrete indices. (This includes
               `_all` string or when no indices have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
        :param ignore_indices: When performed on multiple indices, allows to
               ignore `missing` ones (default: none)
        :param ignore_unavailable: Whether specified concrete indices should be
               ignored when unavailable (missing or closed)
        :param index: A comma-separated list of index name to limit the
               operation
        :param recycler: Clear the recycler cache
        """
        params = {}
        if recycler is not default:
            params['recycler'] = bool(recycler)
        if id_cache is not default:
            params['id_cache'] = bool(id_cache)
        if id is not default:
            params['id'] = bool(id)
        if filter_keys is not default:
            params['filter_keys'] = filter_keys
        if filter_cache is not default:
            params['filter_cache'] = bool(filter_cache)
        if filter is not default:
            params['filter'] = bool(filter)
        if fields is not default:
            params['fields'] = fields
        if field_data is not default:
            params['field_data'] = bool(field_data)
        if fielddata is not default:
            params['fielddata'] = bool(fielddata)
        if ignore_indices is not default:
            params['ignore_indices'] = ignore_indices
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            if not isinstance(expand_wildcards, str):
                raise TypeError("'expand_wildcards' parameter is not a string")
            elif expand_wildcards.lower() in ('open', 'closed'):
                params['expand_wildcards'] = expand_wildcards.lower()
            else:
                raise ValueError("'expand_wildcards' parameter should be one"
                                 " of 'open', 'closed'")
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)

        _, data = yield from self.transport.perform_request(
            'POST', _make_path(index, '_cache', 'clear'),
            params=params)
        return data

    @asyncio.coroutine
    def recovery(self, index=None, *,
                 active_only=default, detailed=default, human=default):
        """
        The indices recovery API provides insight into on-going shard
        recoveries. Recovery status may be reported for specific indices, or
        cluster-wide.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/
        reference/master/indices-recovery.html>`_

        :param index: A comma-separated list of index names; use `_all` or
               empty string to perform the operation on all indices
        :param active_only: Display only those recoveries that are currently
               on-going (default: 'false')
        :param detailed: Whether to display detailed information about shard
               recovery (default: 'false')
        :param human: Whether to return time and byte values in human-readable
               format. (default: 'false')
        """
        params = {}
        if active_only is not default:
            params['active_only'] = bool(active_only)
        if detailed is not default:
            params['detailed'] = bool(detailed)
        if human is not default:
            params['human'] = bool(human)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_recovery'), params=params)
        return data
