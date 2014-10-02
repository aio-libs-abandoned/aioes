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
        """Run analyze tool.

        Perform the analysis process on a text and return the tokens
        breakdown of the text.

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
        """Refresh index.

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
        """Explicitly flush one or more indices."""
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
        """Create an index in Elasticsearch."""
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
        """Open a closed index to make it available for search."""
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
        """Close index.

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
        """Return a boolean indicating whether given index exists."""
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
        """Check if a type/types exists in an index/indices."""
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
    def put_mapping(self, index, doc_type, body, *,
                    allow_no_indices=default, expand_wildcards=default,
                    ignore_conflicts=default, ignore_unavailable=default,
                    master_timeout=default, timeout=default):
        """Register specific mapping definition for a specific type."""
        params = {}
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            params['expand_wildcards'] = bool(expand_wildcards)
        if ignore_conflicts is not default:
            params['ignore_conflicts'] = bool(ignore_conflicts)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if timeout is not default:
            params['timeout'] = timeout

        _, data = yield from self.transport.perform_request(
            'PUT', _make_path(index, '_mapping', doc_type),
            params=params, body=body)
        return data

    @asyncio.coroutine
    def get_mapping(self, index, doc_type=None, *,
                    ignore_unavailable=default, allow_no_indices=default,
                    expand_wildcards=default, local=default):
        """Retrieve mapping definition of index or index/type."""
        params = {}
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            params['expand_wildcards'] = bool(expand_wildcards)
        if local is not default:
            params['local'] = bool(local)
        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_mapping', doc_type),
            params=params
        )
        return data

    @asyncio.coroutine
    def delete_mapping(self, index, doc_type, *,
                       master_timeout=default):
        """Delete a mapping (type) along with its data."""
        params = {}
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        _, data = yield from self.transport.perform_request(
            'DELETE', _make_path(index, '_mapping', doc_type),
            params=params
        )
        return data

    @asyncio.coroutine
    def get_field_mapping(self, field, index=None, doc_type=None, *,
                          include_defaults=default, ignore_unavailable=default,
                          allow_no_indices=default, expand_wildcards=default,
                          local=default):
        """
        Retrieve mapping definition of a specific field.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-get-field-mapping.html>`_

        :arg index: A comma-separated list of index names; use `_all` or empty
            string for all indices
        :arg doc_type: A comma-separated list of document types
        :arg field: A comma-separated list of fields to retrieve the
            mapping for
        :arg include_defaults: A boolean indicating whether to return
            default values
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes
            `_all` string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.
        :arg ignore_unavailable: Whether specified concrete indices should
            be ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
        params = {}
        if include_defaults is not default:
            params['include_defaults'] = bool(include_defaults)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            params['expand_wildcards'] = bool(expand_wildcards)
        if local is not default:
            params['local'] = bool(local)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_mapping', doc_type, 'field', field),
            params=params
        )
        return data

    @asyncio.coroutine
    def put_alias(self, name, index=None, body=None, *,
                  timeout=default, master_timeout=default):
        """
        Create an alias for a specific index/indices.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

        :arg index: A comma-separated list of index names the alias should
            point to (supports wildcards); use `_all` or omit to perform the
            operation on all indices.
        :arg name: The name of the alias to be created or updated
        :arg body: The settings for the alias, such as `routing` or `filter`
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit timestamp for the document
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = master_timeout

        _, data = yield from self.transport.perform_request(
            'PUT', _make_path(index, '_alias', name),
            params=params, body=body
        )
        return data

    @asyncio.coroutine
    def exists_alias(self, name, index=None, *, allow_no_indices=default,
                     expand_wildcards=default, ignore_indices=default,
                     ignore_unavailable=default, local=default):
        """
        Return a boolean indicating whether given alias exists.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

        :arg name: A comma-separated list of alias names to return
        :arg index: A comma-separated list of index names to filter aliases
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes
            `_all` string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression
            to concrete indices that are open, closed or both.
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones (default: none)
        :arg ignore_unavailable: Whether specified concrete indices should
            be ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
        params = {}
        if ignore_indices is not default:
            params['ignore_indices'] = bool(ignore_indices)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            params['expand_wildcards'] = bool(expand_wildcards)
        if local is not default:
            params['local'] = bool(local)

        try:
            yield from self.transport.perform_request(
                'HEAD', _make_path(index, '_alias', name),
                params=params
            )
        except NotFoundError:
            return False
        return True

    @asyncio.coroutine
    def get_alias(self, index=None, name=None, *, allow_no_indices=default,
                  expand_wildcards=default, ignore_indices=default,
                  ignore_unavailable=default, local=default):
        """
        Retrieve a specified alias.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

        :arg name: A comma-separated list of alias names to return
        :arg index: A comma-separated list of index names to filter aliases
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes
            `_all` string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression
            to concrete indices that are open, closed or both.
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones, default u'none'
        :arg ignore_unavailable: Whether specified concrete indices should
            be ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
        params = {}
        if ignore_indices is not default:
            params['ignore_indices'] = bool(ignore_indices)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            params['expand_wildcards'] = bool(expand_wildcards)
        if local is not default:
            params['local'] = bool(local)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_alias', name),
            params=params
        )
        return data

    @asyncio.coroutine
    def get_aliases(self, index=None, name=None, *, local=default,
                    timeout=default):
        """
        Retrieve specified aliases
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

        :arg index: A comma-separated list of index names to filter aliases
        :arg name: A comma-separated list of alias names to filter
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg timeout: Explicit operation timeout
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if local is not default:
            params['local'] = bool(local)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, '_aliases', name),
            params=params
        )
        return data

    @asyncio.coroutine
    def update_aliases(self, body, *, timeout=default,
                       master_timeout=default):
        """
        Update specified aliases.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

        :arg body: The definition of `actions` to perform
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Request timeout
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = bool(master_timeout)

        _, data = yield from self.transport.perform_request(
            'POST', '/_aliases',
            params=params, body=body
        )
        return data

    @asyncio.coroutine
    def delete_alias(self, index, name, *, timeout=default,
                     master_timeout=default):
        """
        Delete specific alias.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

        :arg index: A comma-separated list of index names (supports wildcards);
            use `_all` for all indices
        :arg name: A comma-separated list of aliases to delete (supports
            wildcards); use `_all` to delete all aliases for the
            specified indices.
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit timestamp for the document
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = bool(master_timeout)

        _, data = yield from self.transport.perform_request(
            'DELETE', _make_path(index, '_alias', name),
            params=params
        )
        return data

    @asyncio.coroutine
    def put_template(self, name, body, *, create=default, order=default,
                     timeout=default, master_timeout=default,
                     flat_settings=default):
        """
        Create an index template that will automatically be applied to new
        indices created.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-templates.html>`_

        :arg name: The name of the template
        :arg body: The template definition
        :arg create: Whether the index template should only be added if new or
            can also replace an existing one
        :arg order: The order for this template when merging multiple matching
            ones (higher numbers are merged later, overriding the
            lower numbers)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg flat_settings: Return settings in flat format (default: false)
        """
        params = {}

        if create is not default:
            params['create'] = create
        if order is not default:
            params['order'] = order
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if flat_settings is not default:
            params['flat_settings'] = bool(flat_settings)

        _, data = yield from self.transport.perform_request(
            'PUT', _make_path('_template', name),
            params=params, body=body
        )
        return data

    @asyncio.coroutine
    def exists_template(self, name, *, local=default):
        """
        Return a boolean indicating whether given template exists.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-templates.html>`_

        :arg name: The name of the template
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
        params = {}
        if local is not default:
            params['local'] = bool(local)

        try:
            yield from self.transport.perform_request(
                'HEAD', _make_path('_template', name),
                params=params
            )
        except NotFoundError:
            return False
        return True

    @asyncio.coroutine
    def get_template(self, name=None, *, flat_settings=default,
                     local=default):
        """
        Retrieve an index template by its name.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-templates.html>`_

        :arg name: The name of the template
        :arg flat_settings: Return settings in flat format (default: false)
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
        params = {}
        if local is not default:
            params['local'] = bool(local)
        if flat_settings is not default:
            params['flat_settings'] = bool(flat_settings)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path('_template', name),
            params=params
        )
        return data

    @asyncio.coroutine
    def delete_template(self, name, *, timeout=default,
                        master_timeout=default):
        """
        Delete an index template by its name.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-templates.html>`_

        :arg name: The name of the template
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        params = {}
        if timeout is not default:
            params['timeout'] = timeout
        if master_timeout is not default:
            params['master_timeout'] = master_timeout

        _, data = yield from self.transport.perform_request(
            'DELETE', _make_path('_template', name),
            params=params
        )
        return data

    @asyncio.coroutine
    def get_settings(self, index=None, name=None, *,
                     expand_wildcards=default, ignore_indices=default,
                     ignore_unavailable=default, flat_settings=default,
                     local=default):
        """Retrieve settings for one or more (or all) indices."""
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
        """Change specific index level settings in real time."""
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

    @asyncio.coroutine
    def put_warmer(self, name, body, index=None, doc_type=None, *,
                   allow_no_indices=default, expand_wildcards=default,
                   ignore_unavailable=default, master_timeout=default):
        """
        Create an index warmer to run registered search requests to warm up the
        index before it is available for search.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-warmers.html>`_

        :arg name: The name of the warmer
        :arg body: The search request definition for the warmer
            (query, filters, facets, sorting, etc)
        :arg index: A comma-separated list of index names to register
            the warmer for; use `_all` or omit to perform the operation
            on all indices
        :arg doc_type: A comma-separated list of document types to register the
            warmer for; leave empty to perform the operation on all types
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices in the search request
            to warm. (This includes `_all` string or when no indices have been
            specified)
        :arg expand_wildcards: Whether to expand wildcard expression
            to concrete indices that are open, closed or both, in the
            search request to warm., default u'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed) in the search request
            to warm
        :arg master_timeout: Specify timeout for connection to master
        """
        params = {}

        if master_timeout is not default:
            params['master_timeout'] = master_timeout
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            params['expand_wildcards'] = bool(expand_wildcards)

        if doc_type and not index:
            index = '_all'
        _, data = yield from self.transport.perform_request(
            'PUT', _make_path(index, doc_type, '_warmer', name),
            params=params, body=body
        )
        return data

    @asyncio.coroutine
    def get_warmer(self, index=None, doc_type=None, name=None, *,
                   allow_no_indices=default, expand_wildcards=default,
                   ignore_unavailable=default, local=default):
        """
        Retreieve an index warmer.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-warmers.html>`_

        :arg index: A comma-separated list of index names to restrict the
            operation; use `_all` to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to restrict the
            operation; leave empty to perform the operation on all types
        :arg name: The name of the warmer (supports wildcards); leave empty to
            get all warmers
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression
            to concrete indices that are open, closed or both. default u'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
        params = {}

        if local is not default:
            params['local'] = bool(local)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            params['expand_wildcards'] = bool(expand_wildcards)

        _, data = yield from self.transport.perform_request(
            'GET', _make_path(index, doc_type, '_warmer', name),
            params=params
        )
        return data

    @asyncio.coroutine
    def delete_warmer(self, index, name, *, master_timeout=default):
        """
        Delete an index warmer.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-warmers.html>`_

        :arg index: A comma-separated list of index names to delete
            warmers from (supports wildcards); use `_all` to perform
            the operation on all indices.
        :arg name: A comma-separated list of warmer names to delete (supports
            wildcards); use `_all` to delete all warmers in the
            specified indices.
        :arg master_timeout: Specify timeout for connection to master
        """
        params = {}

        if master_timeout is not default:
            params['master_timeout'] = master_timeout

        _, data = yield from self.transport.perform_request(
            'DELETE', _make_path(index, '_warmer', name),
            params=params
        )
        return data

    @asyncio.coroutine
    def snapshot_index(self, index=None, *, allow_no_indices=default,
                       expand_wildcards=default, ignore_indices=default,
                       ignore_unavailable=default):
        """
        Explicitly perform a snapshot through the gateway of one or more
        indices (backup them).
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-gateway-snapshot.html>`_

        :arg index: A comma-separated list of index names; use `_all` or empty
            string for all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes
            `_all` string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression
            to concrete indices that are open, closed or both.
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones (default: none)
        :arg ignore_unavailable: Whether specified concrete indices should
            be ignored when unavailable (missing or closed)
        """
        params = {}

        if ignore_indices is not default:
            params['ignore_indices'] = bool(ignore_unavailable)
        if ignore_unavailable is not default:
            params['ignore_unavailable'] = bool(ignore_unavailable)
        if allow_no_indices is not default:
            params['allow_no_indices'] = bool(allow_no_indices)
        if expand_wildcards is not default:
            params['expand_wildcards'] = bool(expand_wildcards)

        _, data = yield from self.transport.perform_request(
            'POST',
            _make_path(index, '_gateway', 'snapshot'), params=params
        )
        return data

    @asyncio.coroutine
    def status(self, index=None, *,
               allow_no_indices=default, expand_wildcards=default,
               ignore_indices=default, ignore_unavailable=default,
               operation_threading=default, recovery=default, snapshot=default,
               human=default):
        """Get a comprehensive status information of one or more indices."""
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
        """Retrieve statistics on operations happening on an index."""
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
        """Get segments information.

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
        """Explicitly optimize one or more indices through an API."""
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
        """Validate a potentially expensive query without executing it."""
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
        """Clear cache.

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
        """Recover an index.

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
