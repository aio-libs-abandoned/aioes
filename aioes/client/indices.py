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
        """Delete an index in Elasticsearch."""
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

    @asyncio.coroutine
    def put_mapping(self, doc_type, body, *, index=None, params=None):
        """
        Register specific mapping definition for a specific type.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-put-mapping.html>`_
        """
        _, data = yield from self.transport.perform_request(
            'PUT', _make_path(index, '_mapping', doc_type),
            params=params, body=body
        )
        return data

    @asyncio.coroutine
    def get_mapping(self, index, doc_type, params=None):
        """
        Retrieve mapping definition of index or index/type.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-get-mapping.html>`_
        """
        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_mapping', doc_type),
            params=params
        )
        return data

    @asyncio.coroutine
    def delete_mapping(self, index, doc_type, params=None):
        """
        Delete a mapping (type) along with its data.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-delete-mapping.html>`_
        """
        _, data = yield from self.transport.perform_request(
            'DELETE', _make_path(index, '_mapping', doc_type),
            params=params
        )
        return data
    #
    # @asyncio.coroutine
    # def get_field_mapping(self):
    #     pass
    #
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
