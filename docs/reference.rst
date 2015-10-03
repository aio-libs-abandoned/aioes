aioes reference
================

.. module:: aioes
   :synopsis: A library for accessing Elasticsearch server.
.. currentmodule:: aioes


Elasticsearch
-----------------

.. class:: Elasticsearch

   Class for operating on Elasticsearch cluster.

   .. method:: ping()

      A :ref:`coroutine <coroutine>` that returns True if the cluster is up,
      False otherwise.

      :returns: bool


   .. method:: info()

      A :ref:`coroutine <coroutine>` that returns basic info from the
      current cluster.

      :returns: resulting JSON


   .. method:: index(index, doc_type, body, id=None, *, \
                     consistency=default, op_type=default, parent=default, \
                     refresh=default, replication=default, routing=default, \
                     timeout=default, timestamp=default, ttl=default, \
                     version=default, version_type=default)

      A :ref:`coroutine <coroutine>` that adds or updates a typed JSON
      document in a specific index, making it searchable.

      :arg index: The name of the index
      :arg doc_type: The type of the document
      :arg body: The document
      :arg id: Document ID
      :arg consistency: Explicit write consistency setting for the operation
      :arg op_type: Explicit operation type (default: index)
      :arg parent: ID of the parent document
      :arg refresh: Refresh the index after performing the operation
      :arg replication: Specific replication type (default: sync)
      :arg routing: Specific routing value
      :arg timeout: Explicit operation timeout
      :arg timestamp: Explicit timestamp for the document
      :arg ttl: Expiration time for the document
      :arg version: Explicit version number for concurrency control
      :arg version_type: Specific version type

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-index_.html>`_


   .. method:: create(index, doc_type, body, id=None, *, consistency=default, \
                      parent=default, percolate=default, refresh=default, \
                      replication=default, routing=default, timeout=default, \
                      timestamp=default, ttl=default, version=default, \
                      version_type=default)

      A :ref:`coroutine <coroutine>` that adds a typed JSON document in a
      specific index, making it searchable.
      Behind the scenes this method calls index(..., op_type='create')

      :arg index: The name of the index
      :arg doc_type: The type of the document
      :arg id: Document ID
      :arg body: The document
      :arg consistency: Explicit write consistency setting for the operation
      :arg id: Specific document ID (when the POST method is used)
      :arg parent: ID of the parent document
      :arg percolate: Percolator queries to execute while indexing the document
      :arg refresh: Refresh the index after performing the operation
      :arg replication: Specific replication type (default: sync)
      :arg routing: Specific routing value
      :arg timeout: Explicit operation timeout
      :arg timestamp: Explicit timestamp for the document
      :arg ttl: Expiration time for the document
      :arg version: Explicit version number for concurrency control
      :arg version_type: Specific version type

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: exists(index, id, doc_type='_all', *, parent=default, \
                      preference=default, realtime=default, refresh=default, \
                      routing=default)

      A :ref:`coroutine <coroutine>` that returns a boolean indicating
      whether or not given document exists in Elasticsearch.

      :arg index: The name of the index
      :arg id: The document ID
      :arg doc_type: The type of the document (uses `_all` by default to
             fetch the first document matching the ID across all types)
      :arg parent: The ID of the parent document
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg realtime: Specify whether to perform the operation in realtime or
             search mode
      :arg refresh: Refresh the shard containing the document before
             performing the operation
      :arg routing: Specific routing value

      :returns: bool

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: get(index, id, doc_type='_all', *, _source=default,\
                   _source_exclude=default, _source_include=default, \
                   fields=default, parent=default, preference=default, \
                   realtime=default, refresh=default, routing=default, \
                   version=default, version_type=default)

      A :ref:`coroutine <coroutine>` that get a typed JSON document from the
      index based on its id.

      :arg index: The name of the index
      :arg id: The document ID
      :arg doc_type: The type of the document (uses `_all` by default to
             fetch the first document matching the ID across all types)
      :arg _source: True or false to return the _source field or not, or a
             list of fields to return
      :arg _source_exclude: A list of fields to exclude from the returned
             _source field
      :arg _source_include: A list of fields to extract and return from the
             _source field
      :arg fields: A comma-separated list of fields to return in the response
      :arg parent: The ID of the parent document
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg realtime: Specify whether to perform the operation in realtime or
             search mode
      :arg refresh: Refresh the shard containing the document before
             performing the operation
      :arg routing: Specific routing value
      :arg version: Explicit version number for concurrency control
      :arg version_type: Explicit version number for concurrency control

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: mget(body, index=None, doc_type=None, *, _source=default, \
                    _source_exclude=default, _source_include=default, \
                    fields=default, parent=default, preference=default, \
                    realtime=default, refresh=default, routing=default)

      A :ref:`coroutine <coroutine>` that get multiple documents based on an index,
      type (optional) and ids.

      :arg body: Document identifiers; can be either `docs` (containing full
             document information) or `ids` (when index and type is provided in the URL.
      :arg index: The name of the index
      :arg doc_type: The type of the document
      :arg _source: True or false to return the _source field or not, or a
             list of fields to return
      :arg _source_exclude: A list of fields to exclude from the returned
             _source field
      :arg _source_include: A list of fields to extract and return from the
             _source field
      :arg fields: A comma-separated list of fields to return in the response
      :arg parent: The ID of the parent document
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg realtime: Specify whether to perform the operation in realtime or
             search mode
      :arg refresh: Refresh the shard containing the document before
             performing the operation
      :arg routing: Specific routing value

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: get_source(index, id, doc_type='_all', *, _source=default, \
                          _source_exclude=default, _source_include=default, \
                          parent=default, preference=default, realtime=default,\
                          refresh=default, routing=default, version=default, \
                          version_type=default)

      A :ref:`coroutine <coroutine>` that get the source of a document by it's
      index, type and id.

      :arg index: The name of the index
      :arg doc_type: The type of the document (uses `_all` by default to
             fetch the first document matching the ID across all types)
      :arg id: The document ID
      :arg _source: True or false to return the _source field or not, or a
             list of fields to return
      :arg _source_exclude: A list of fields to exclude from the returned
             _source field
      :arg _source_include: A list of fields to extract and return from the
             _source field
      :arg parent: The ID of the parent document
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg realtime: Specify whether to perform the operation in realtime
             or search mode
      :arg refresh: Refresh the shard containing the document before
             performing the operation
      :arg routing: Specific routing value
      :arg version: Explicit version number for concurrency control
      :arg version_type: Explicit version number for concurrency control

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: update(index, doc_type, id, body=None, *, \
                      consistency=default, fields=default, lang=default,\
                      parent=default, refresh=default, \
                      replication=default, retry_on_conflict=default, \
                      routing=default, script=default, timeout=default,\
                      timestamp=default, ttl=default, version=default, \
                      version_type=default)

      A :ref:`coroutine <coroutine>` that update a document based on a script or partial data provided.

      :arg index: The name of the index
      :arg doc_type: The type of the document
      :arg id: Document ID
      :arg body: The request definition using either `script` or partial `doc`
      :arg consistency: Explicit write consistency setting for the operation
      :arg fields: A comma-separated list of fields to return in the response
      :arg lang: The script language (default: mvel)
      :arg parent: ID of the parent document
      :arg refresh: Refresh the index after performing the operation
      :arg replication: Specific replication type (default: sync)
      :arg retry_on_conflict: Specify how many times should the operation be
             retried when a conflict occurs (default: 0)
      :arg routing: Specific routing value
      :arg script: The URL-encoded script definition (instead of using request body)
      :arg timeout: Explicit operation timeout
      :arg timestamp: Explicit timestamp for the document
      :arg ttl: Expiration time for the document
      :arg version: Explicit version number for concurrency control
      :arg version_type: Explicit version number for concurrency control

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-update.html>`_


   .. method:: search(index=None, doc_type=None, body=None, *, \
                      _source=default, _source_exclude=default, \
                      _source_include=default, analyze_wildcard=default, \
                      analyzer=default, default_operator=default, df=default, \
                      explain=default, fields=default, indices_boost=default, \
                      lenient=default, allow_no_indices=default, \
                      expand_wildcards=default, ignore_unavailable=default, \
                      lowercase_expanded_terms=default, from_=default, \
                      preference=default, q=default, routing=default, \
                      scroll=default, search_type=default, size=default, \
                      sort=default, source=default, stats=default, \
                      suggest_field=default, suggest_mode=default, \
                      suggest_size=default, suggest_text=default, \
                      timeout=default, version=default)

      A :ref:`coroutine <coroutine>` that execute a search query and get back
      search hits that match the query.

      :arg index: A comma-separated list of index names to search; use `_all`
            or empty string to perform the operation on all indices
      :arg doc_type: A comma-separated list of document types to search;
            leave empty to perform the operation on all types
      :arg body: The search definition using the Query DSL
      :arg _source: True or false to return the _source field or not, or a
            list of fields to return
      :arg _source_exclude: A list of fields to exclude from the returned
            _source field
      :arg _source_include: A list of fields to extract and return from the
            _source field
      :arg analyze_wildcard: Specify whether wildcard and prefix queries
            should be analyzed (default: false)
      :arg analyzer: The analyzer to use for the query string
      :arg default_operator: The default operator for query string query (AND
            or OR) (default: OR)
      :arg df: The field to use as default where no field prefix is given in
            the query string
      :arg explain: Specify whether to return detailed information about
            score computation as part of a hit
      :arg fields: A comma-separated list of fields to return as part of a hit
      :arg indices_boost: Comma-separated list of index boosts
      :arg lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
      :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
      :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
      :arg lowercase_expanded_terms: Specify whether query terms should be lowercased
      :arg from\_: Starting offset (default: 0)
      :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
      :arg q: Query in the Lucene query string syntax
      :arg routing: A comma-separated list of specific routing values
      :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
      :arg search_type: Search operation type
      :arg size: Number of hits to return (default: 10)
      :arg sort: A comma-separated list of <field>:<direction> pairs
      :arg source: The URL-encoded request definition using the Query DSL
            (instead of using request body)
      :arg stats: Specific 'tag' of the request for logging and statistical purposes
      :arg suggest_field: Specify which field to use for suggestions
      :arg suggest_mode: Specify suggest mode (default: missing)
      :arg suggest_size: How many suggestions to return in response
      :arg suggest_text: The source text for which the suggestions should be returned
      :arg timeout: Explicit operation timeout
      :arg version: Specify whether to return document version as part of a hit

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-search.html>`_


   .. method:: search_shards(index=None, doc_type=None, *, \
                             allow_no_indices=default, \
                             expand_wildcards=default,\
                             ignore_unavailable=default, \
                             local=default, preference=default, \
                             routing=default)

      A :ref:`coroutine <coroutine>` that returns the indices and shards that a search
      request would be executed against. This can give useful feedback for working
      out issues or planning optimizations with routing and shard preferences
      execute a search query and get back search hits that match the query.

      :arg index: The name of the index
      :arg doc_type: The type of the document
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both. (default: '"open"')
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :arg local: Return local information, do not retrieve the state from
             master node (default: false)
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg routing: Specific routing value

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-shards.html>`_


   .. method:: search_template(index=None, doc_type=None, body=None, *, \
                               allow_no_indices=default, \
                               expand_wildcards=default, \
                               ignore_unavailable=default, preference=default, \
                               routing=default, scroll=default, \
                               search_type=default)

      A :ref:`coroutine <coroutine>` that accepts a body with a query template and
      a map of key/value pairs to fill in template parameters.

      :arg index: A comma-separated list of index names to search; use `_all`
             or empty string to perform the operation on all indices
      :arg doc_type: A comma-separated list of document types to search; leave
             empty to perform the operation on all types
      :arg body: The search definition template and its params
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg routing: A comma-separated list of specific routing values
      :arg scroll: Specify how long a consistent view of the index should be
             maintained for scrolled search
      :arg search_type: Search operation type

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl-template-query.html>`_


   .. method:: explain(index, doc_type, id, body=None, *, \
                       _source=default, _source_exclude=default, \
                       _source_include=default, analyze_wildcard=default,\
                       analyzer=default, default_operator=default, \
                       df=default, fields=default, lenient=default,\
                       lowercase_expanded_terms=default, parent=default,\
                       preference=default, q=default, routing=default,\
                       source=default)

      A :ref:`coroutine <coroutine>` that computes a score explanation for a
      query and a specific document. This can give useful feedback whether a
      document matches or didn't match a specific query.

      :arg index: The name of the index
      :arg doc_type: The type of the document
      :arg id: The document ID
      :arg body: The query definition using the Query DSL
      :arg _source: True or false to return the _source field or not, or a
             list of fields to return
      :arg _source_exclude: A list of fields to exclude from the returned
             _source field
      :arg _source_include: A list of fields to extract and return from the
             _source field
      :arg analyze_wildcard: Specify whether wildcards and prefix queries in
             the query string query should be analyzed (default: false)
      :arg analyzer: The analyzer for the query string query
      :arg default_operator: The default operator for query string query (AND
             or OR), (default: OR)
      :arg df: The default field for query string query (default: _all)
      :arg fields: A comma-separated list of fields to return in the response
      :arg lenient: Specify whether format-based query failures (such as
             providing text to a numeric field) should be ignored
      :arg lowercase_expanded_terms: Specify whether query terms should be lowercased
      :arg parent: The ID of the parent document
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg q: Query in the Lucene query string syntax
      :arg routing: Specific routing value
      :arg source: The URL-encoded query definition (instead of using the
             request body)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-explain.html>`_


   .. method:: scroll(scroll_id, *, scroll=default)

      A :ref:`coroutine <coroutine>` that scroll a search request created by
      specifying the scroll parameter

      :arg scroll_id: The scroll ID
      :arg scroll: Specify how long a consistent view of the index should be
             maintained for scrolled search

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_


   .. method:: clear_scroll(scroll_id=None, body=None)

      A :ref:`coroutine <coroutine>` that clear the scroll request created
      by specifying the scroll parameter to search.

      :arg scroll_id: The scroll ID or a list of scroll IDs
      :arg body: A comma-separated list of scroll IDs to clear if none was
             specified via the scroll_id parameter

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_


   .. method:: delete(index, doc_type, id, *, consistency=default, \
                      parent=default, refresh=default,\
                      replication=default, routing=default, \
                      timeout=default, version=default, \
                      version_type=default)

      A :ref:`coroutine <coroutine>` that delete a typed JSON document from
      a specific index based on its id.

      :arg index: The name of the index
      :arg doc_type: The type of the document
      :arg id: The document ID
      :arg consistency: Specific write consistency setting for the operation
      :arg parent: ID of parent document
      :arg refresh: Refresh the index after performing the operation
      :arg replication: Specific replication type (default: sync)
      :arg routing: Specific routing value
      :arg timeout: Explicit operation timeout
      :arg version: Explicit version number for concurrency control
      :arg version_type: Specific version type

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-delete.html>`_


   .. method:: count(index=None, doc_type=None, body=None, *, \
                     allow_no_indices=default, expand_wildcards=default,\
                     ignore_unavailable=default, min_score=default,\
                     preference=default, q=default, routing=default,\
                     source=default)

      A :ref:`coroutine <coroutine>` that execute a query and get the
      number of matches for that query.

      :arg index: A comma-separated list of indices to restrict the results
      :arg doc_type: A comma-separated list of types to restrict the results
      :arg body: A query to restrict the results (optional)
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :arg min_score: Include only documents with a specific `_score` value
             in the result
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg q: Query in the Lucene query string syntax
      :arg routing: Specific routing value
      :arg source: The URL-encoded query definition (instead of using the request body)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-count.html>`_


   .. method:: bulk(body, index=None, doc_type=None, *, consistency=default,\
                    refresh=default, routing=default, replication=default, \
                    timeout=default)

      A :ref:`coroutine <coroutine>` that perform many index/delete
      operations in a single API call.

      :arg body: The operation definition and data (action-data pairs), as
             either a newline separated string, or a sequence of dicts to
             serialize (one per row).
      :arg index: Default index for items which don't provide one
      :arg doc_type: Default document type for items which don't provide one
      :arg consistency: Explicit write consistency setting for the operation
      :arg refresh: Refresh the index after performing the operation
      :arg routing: Specific routing value
      :arg replication: Explicitly set the replication type (default: sync)
      :arg timeout: Explicit operation timeout

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-bulk.html>`_


   .. method:: msearch(body, index=None, doc_type=None, *, \
                       search_type=default)

      A :ref:`coroutine <coroutine>` that executes several search requests
      within the same API.

      :arg body: The request definitions (metadata-search request definition
             pairs), as either a newline separated string, or a sequence of
             dicts to serialize (one per row).
      :arg index: A comma-separated list of index names to use as default
      :arg doc_type: A comma-separated list of document types to use as default
      :arg search_type: Search operation type

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-multi-search.html>`_


   .. method:: delete_by_query(index, doc_type=None, body=None, *, \
                               allow_no_indices=default, analyzer=default, \
                               consistency=default, default_operator=default,\
                               df=default, expand_wildcards=default, \
                               ignore_unavailable=default, q=default, \
                               replication=default, routing=default, \
                               source=default, timeout=default)

      A :ref:`coroutine <coroutine>` that delete documents from one or more
      indices and one or more types based on a query.

      :arg index: A comma-separated list of indices to restrict the operation;
             use `_all` to perform the operation on all indices
      :arg doc_type: A comma-separated list of types to restrict the operation
      :arg body: A query to restrict the operation specified with the Query
             DSL
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :arg analyzer: The analyzer to use for the query string
      :arg consistency: Specific write consistency setting for the operation
      :arg default_operator: The default operator for query string query (AND
             or OR), default u'OR'
      :arg df: The field to use as default where no field prefix is given in
             the query string
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default u'open'
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :arg q: Query in the Lucene query string syntax
      :arg replication: Specific replication type, default u'sync'
      :arg routing: Specific routing value
      :arg source: The URL-encoded query definition (instead of using the
             request body)
      :arg timeout: Explicit operation timeout

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-delete-by-query.html>`_



   .. method:: suggest(index, body, *, allow_no_indices=default,\
                       expand_wildcards=default, ignore_unavailable=default,\
                       preference=default, routing=default, source=default)

      A :ref:`coroutine <coroutine>` that suggests similar looking terms based on a provided
      text by using a suggester.

      :arg index: A comma-separated list of index names to restrict the operation;
             use `_all` or empty string to perform the operation on all indices
      :arg body: The request definition
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg routing: Specific routing value
      :arg source: The URL-encoded request definition (instead of using request body)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-search.html>`_


   .. method:: percolate(index, doc_type, id=None, body=None, *, \
                         allow_no_indices=default, expand_wildcards=default,\
                         ignore_unavailable=default, percolate_format=default,\
                         percolate_index=default, percolate_type=default,\
                         preference=default, routing=default, version=default,\
                         version_type=default)

      A :ref:`coroutine <coroutine>` that allows to register queries against
      an index, and then send percolate requests which include a doc, and getting
      back the queries that match on that doc out of the set of registered queries.

      :arg index: The index of the document being percolated.
      :arg doc_type: The type of the document being percolated.
      :arg id: Substitute the document in the request body with a document
             that is known by the specified id. On top of the id, the index and
             type parameter will be used to retrieve the document from within the
             cluster.
      :arg body: The percolator request definition using the percolate DSL
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :arg percolate_format: Return an array of matching query IDs instead of
             objects
      :arg percolate_index: The index to percolate the document into. Defaults
             to index.
      :arg percolate_type: The type to percolate document into. Defaults to
             type.
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg routing: A comma-separated list of specific routing values
      :arg version: Explicit version number for concurrency control
      :arg version_type: Specific version type

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_


   .. method:: mpercolate(body, index=None, doc_type=None, *, \
                          allow_no_indices=default, expand_wildcards=default, \
                          ignore_unavailable=default)

      A :ref:`coroutine <coroutine>` that allows to register queries against
      an index, and then send percolate requests which include a doc, and getting
      back the queries that match on that doc out of the set of registered queries.

      :arg index: The index of the document being count percolated to use as
             default
      :arg doc_type: The type of the document being percolated to use as
             default.
      :arg body: The percolate request definitions (header & body pair),
             separated by newlines
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_


   .. method:: count_percolate(index, doc_type, id=None, body=None, *, \
                               allow_no_indices=default, \
                               expand_wildcards=default, \
                               ignore_unavailable=default, \
                               percolate_index=default, \
                               percolate_type=default, preference=default, \
                               routing=default, version=default, \
                               version_type=default)

      A :ref:`coroutine <coroutine>` that allows to register queries against an
      index, and then send percolate requests which include a doc, and getting back
      the queries that match on that doc out of the set of registered queries.

      :arg index: The index of the document being count percolated.
      :arg doc_type: The type of the document being count percolated.
      :arg id: Substitute the document in the request body with a document
             that is known by the specified id. On top of the id, the index and
             type parameter will be used to retrieve the document from within the
             cluster.
      :arg body: The count percolator request definition using the percolate DSL
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :arg percolate_index: The index to count percolate the document into.
             Defaults to index.
      :arg percolate_type: The type to count percolate document into. Defaults
             to type.
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random)
      :arg routing: A comma-separated list of specific routing values
      :arg version: Explicit version number for concurrency control
      :arg version_type: Specific version type

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_


   .. method:: mlt(index, doc_type, id, body=None, *, boost_terms=default, \
                   include=default, max_doc_freq=default, \
                   max_query_terms=default, max_word_length=default, \
                   min_doc_freq=default, min_term_freq=default, \
                   min_word_length=default, mlt_fields=default, \
                   percent_terms_to_match=default, routing=default, \
                   search_from=default, search_indices=default, \
                   search_query_hint=default, search_scroll=default, \
                   search_size=default, search_source=default, \
                   search_type=default, search_types=default, stop_words=default)

      A :ref:`coroutine <coroutine>` which get documents that are "like" a specified document

      :arg index: The name of the index
      :arg doc_type: The type of the document (use `_all` to fetch the first
             document matching the ID across all types)
      :arg id: The document ID
      :arg body: A specific search request definition
      :arg boost_terms: The boost factor
      :arg include: Whether to include the queried document from the response
      :arg max_doc_freq: The word occurrence frequency as count: words with
             higher occurrence in the corpus will be ignored
      :arg max_query_terms: The maximum query terms to be included in the generated query
      :arg max_word_length: The minimum length of the word: longer words will be ignored
      :arg min_doc_freq: The word occurrence frequency as count: words with
             lower occurrence in the corpus will be ignored
      :arg min_term_freq: The term frequency as percent: terms with lower
             occurence in the source document will be ignored
      :arg min_word_length: The minimum length of the word: shorter words will be ignored
      :arg mlt_fields: Specific fields to perform the query against
      :arg percent_terms_to_match: How many terms have to match in order to
             consider the document a match (default: 0.3)
      :arg routing: Specific routing value
      :arg search_from: The offset from which to return results
      :arg search_indices: A comma-separated list of indices to perform the
             query against (default: the index containing the document)
      :arg search_query_hint: The search query hint
      :arg search_scroll: A scroll search request definition
      :arg search_size: The number of documents to return (default: 10)
      :arg search_source: A specific search request definition (instead of
             using the request body)
      :arg search_type: Specific search type (eg. `dfs_then_fetch`, `count`, etc)
      :arg search_types: A comma-separated list of types to perform the query
             against (default: the same type as the document)
      :arg stop_words: A list of stop words to be ignored

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-more-like-this.html>`_


   .. method:: termvector(index, doc_type, id, body=None, *, \
                          field_statistics=default, fields=default, \
                          offsets=default, parent=default, payloads=default,\
                          positions=default, preference=default, routing=default,\
                          term_statistics=default)

      A :ref:`coroutine <coroutine>` that returns information and statistics on
      terms in the fields of a particular document as stored in the index.

      :arg index: The index in which the document resides.
      :arg doc_type: The type of the document.
      :arg id: The id of the document.
      :arg body: Define parameters. See documentation.
      :arg field_statistics: Specifies if document count, sum of document
             frequencies and sum of total term frequencies should be returned.
             (default True)
      :arg fields: A comma-separated list of fields to return.
      :arg offsets: Specifies if term offsets should be returned. (default True)
      :arg parent: Parent id of documents.
      :arg payloads: Specifies if term payloads should be returned. (default True)
      :arg positions: Specifies if term positions should be returned. (default True)
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random).
      :arg routing: Specific routing value.
      :arg term_statistics: Specifies if total term frequency and document
             frequency should be returned., default False

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-termvectors.html>`_


   .. method:: mtermvectors(index=None, doc_type=None, body=None, *, \
                            field_statistics=default, fields=default, \
                            ids=default, offsets=default, parent=default,\
                            payloads=default, positions=default,\
                            preference=default, routing=default,\
                            term_statistics=default)

      A :ref:`coroutine <coroutine>` allows to get multiple termvectors based on
      an index, type and id.

      :arg index: The index in which the document resides.
      :arg doc_type: The type of the document.
      :arg body: Define ids, parameters or a list of parameters per document
             here. You must at least provide a list of document ids. See
             documentation.
      :arg field_statistics: Specifies if document count, sum of document
             frequencies and sum of total term frequencies should be returned.
             Applies to all returned documents unless otherwise specified in body
             "params" or "docs". (default True)
      :arg fields: A comma-separated list of fields to return. Applies to all
             returned documents unless otherwise specified in body "params" or
             "docs".
      :arg ids: A comma-separated list of documents ids. You must define ids
             as parameter or set "ids" or "docs" in the request body
      :arg offsets: Specifies if term offsets should be returned. Applies to
             all returned documents unless otherwise specified in body "params"
             or "docs". (default True)
      :arg parent: Parent id of documents. Applies to all returned documents
             unless otherwise specified in body "params" or "docs".
      :arg payloads: Specifies if term payloads should be returned. Applies to
             all returned documents unless otherwise specified in body "params"
             or "docs". (default True)
      :arg positions: Specifies if term positions should be returned. Applies
             to all returned documents unless otherwise specified in body
             "params" or "docs". (default True)
      :arg preference: Specify the node or shard the operation should be
             performed on (default: random) .Applies to all returned documents
             unless otherwise specified in body "params" or "docs".
      :arg routing: Specific routing value. Applies to all returned documents
             unless otherwise specified in body "params" or "docs".
      :arg term_statistics: Specifies if total term frequency and document
             frequency should be returned. Applies to all returned documents
             unless otherwise specified in body "params" or "docs". (default
             False)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-multi-termvectors.html>`_


   .. method:: benchmark(index=None, doc_type=None, body=None, *, \
                         verbose=default)

      A :ref:`coroutine <coroutine>` that provides a standard mechanism for
      submitting queries and measuring their performance relative to one another.

      :arg index: A comma-separated list of index names; use `_all` or empty
             string to perform the operation on all indices
      :arg doc_type: The name of the document type
      :arg body: The search definition using the Query DSL
      :arg verbose: Specify whether to return verbose statistics about each
             iteration (default: false)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-benchmark.html>`_


    .. method:: put_script(lang, id, body)

      A :ref:`coroutine <coroutine>` that creates a script in given language with specified ID.

      :arg lang: Script language
      :arg id: Script ID
      :arg body: The document

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_


    .. method:: get_script(lang, id)

      A :ref:`coroutine <coroutine>` that retrieves a script from the API.

      :arg lang: Script language
      :arg id: Script ID

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_


    .. method:: delete_script(lang, id)

      A :ref:`coroutine <coroutine>` that removes a script from the API.

      :arg lang: Script language
      :arg id: Script ID

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_


    .. method:: put_template(id, body)

      A :ref:`coroutine <coroutine>` that creates a search template with specified ID.

      :arg id: Template ID
      :arg body: The document

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_


    .. method:: get_template(id)

      A :ref:`coroutine <coroutine>` that retrieves a search template with specified ID.

      :arg id: Template ID

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_


    .. method:: delete_template(id)

      A :ref:`coroutine <coroutine>` that removes a search template with specified ID.

      :arg id: Template ID

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_


IndicesClient
-----------------


.. class:: aioes.client.IndicesClient

   Class for operating on Elasticsearch indices.

   .. method:: analyze(index=None, body=None, *, analyzer=default, \
                       char_filters=default, field=default, filters=default,\
                       prefer_local=default, text=default, tokenizer=default)

      A :ref:`coroutine <coroutine>` that make analysis process on a text
      and return the tokens breakdown of the text.

      :arg index: The name of the index
      :arg body: The text on which the analysis should be performed
      :arg analyzer: The name of the analyzer to use
      :arg char_filters: A comma-separated list of character filters to use
             for the analysis
      :arg field: Use the analyzer configured for this field (instead of
             passing the analyzer name)
      :arg filters: A comma-separated list of filters to use for the analysis
      :arg prefer_local: With `true`, specify that a local shard should be
             used if available, with `false`, use a random shard (default: true)
      :arg text: The text on which the analysis should be performed (when
             request body is not used)
      :arg tokenizer: The name of the tokenizer to use for the analysis

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-analyze.html>`_


   .. method:: create(index, body=None, *, timeout=default, \
                      master_timeout=default)

      A :ref:`coroutine <coroutine>` that creates an index in Elasticsearch

      :arg index: The name of the index
      :arg body: The configuration for the index (`settings` and `mappings`)
      :arg master_timeout: Specify timeout for connection to master
      :arg timeout: Explicit operation timeout

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-create-index.html>`_


   .. method:: open(index, *, timeout=default, master_timeout=default, \
                    allow_no_indices=default, expand_wildcards=default, \
                    ignore_unavailable=default)

      A :ref:`coroutine <coroutine>` that open a closed index to make it
      available for search.

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

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-open-close.html>`_


   .. method:: close(index, *, allow_no_indices=default, \
                     expand_wildcards=default, ignore_unavailable=default,\
                     master_timeout=default, timeout=default)

      A :ref:`coroutine <coroutine>` that close an index to remove it's overhead from
      the cluster. Closed index is blocked for read/write operations.

      :arg index: The name of the index
      :arg master_timeout: Specify timeout for connection to master
      :arg timeout: Explicit operation timeout
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all` string or
             when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default u'open'
      :arg ignore_unavailable: Whether specified concrete indices should be ignored
             when unavailable (missing or closed)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-open-close.html>`_

   .. method:: delete(index, *, master_timeout=default, timeout=default)

      A :ref:`coroutine <coroutine>` that deletes an index.

      :arg index: A comma-separated list of indices to delete; use ``'_all'``
                    or ``'*'`` to delete all indices
      :arg master_timeout: Specify timeout for connection to master
      :arg timeout: Explicit operation timeout

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-delete-index.html>`_


   .. method:: refresh(index=None, *,\
                       allow_no_indices=default, expand_wildcards=default,\
                       ignore_indices=default, ignore_unavailable=default,\
                       force=default)

      A :ref:`coroutine <coroutine>` that refresh one or more index, making all
      operations performed.

      :arg index: A comma-separated list of index names; use `_all` or
             empty string to perform the operation on all indices
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
               concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows to
               ignore `missing` ones, default u'none'
      :arg ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
      :arg force: Force a refresh even if not required

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-refresh.html>`_

   .. method:: flush(index=None, *,\
                     force=default, full=default, allow_no_indices=default,\
                     expand_wildcards=default, ignore_indices=default,\
                     ignore_unavailable=default)

      A :ref:`coroutine <coroutine>` that flush one or more indices.

      :arg index: A comma-separated list of index names; use `_all` or
             empty string to perform the operation on all indices
      :arg force: Whether a flush should be forced even if it is not
             necessarily needed ie. if no changes will be committed to
             the index.
      :arg full: If set to true a new index writer is created and settings
             that have been changed related to the index writer will be
             refreshed.
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows to
             ignore `missing` ones (default: none)
      :arg ignore_unavailable: Whether specified concrete indices should
             be ignored when unavailable (missing or closed)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-flush.html>`_

   .. method:: exists(index, *, \
               allow_no_indices=default, expand_wildcards=default, \
               ignore_unavailable=default, local=default)

      A :ref:`coroutine <coroutine>` that return a boolean indicating
      whether given index exists.

      :arg index: A list of indices to check
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both., default u'open'
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :arg local: Return local information, do not retrieve the state from
             master node (default: false)

      :returns: resulting bool

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-indices-exists.html>`_

   .. method:: exists_type(index, doc_type, *, \
                           allow_no_indices=default, expand_wildcards=default,\
                           ignore_indices=default, ignore_unavailable=default,\
                           local=default)

      A :ref:`coroutine <coroutine>` that check if a type/types exists
      in an index/indices.

      :arg index: A comma-separated list of index names; use `_all` to
               check the types across all indices
      :arg doc_type: A comma-separated list of document types to check
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows to
             ignore `missing` ones (default: none)
      :arg ignore_unavailable: Whether specified concrete indices should
               be ignored when unavailable (missing or closed)
      :arg local: Return local information, do not retrieve the state from
               master node (default: false)

      :returns: resulting bool

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-types-exists.html>`_

   .. method:: get_settings(index=None, name=None, *, \
                            expand_wildcards=default, ignore_indices=default,\
                            ignore_unavailable=default, flat_settings=default,\
                            local=default)

      A :ref:`coroutine <coroutine>` that retrieve settings for one or
      more (or all) indices.

      :arg index: A comma-separated list of index names; use `_all` or
             empty string to perform the operation on all indices
      :arg name: The name of the settings that should be included
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows to
             ignore `missing` ones, default u'none'
      :arg ignore_unavailable: Whether specified concrete indices should
             be ignored when unavailable (missing or closed)
      :arg flat_settings: Return settings in flat format (default: false)
      :arg local: Return local information, do not retrieve the state from
             master node (default: false)

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-get-settings.html>`_

   .. method:: put_settings(body, index=None, *, \
                            allow_no_indices=default,\
                            expand_wildcards=default,\
                            flat_settings=default,\
                            ignore_unavailable=default,\
                            master_timeout=default)

      A :ref:`coroutine <coroutine>` that change specific index level
      settings in real time.

      :arg body: The index settings to be updated
      :arg index: A comma-separated list of index names; use `_all` or
             empty string to perform the operation on all indices
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both., default
             u'open'
      :arg flat_settings: Return settings in flat format (default: false)
      :arg ignore_unavailable: Whether specified concrete indices should
             be ignored when unavailable (missing or closed)
      :arg master_timeout: Specify timeout for connection to master

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-update-settings.html>`_

   .. method:: status(index=None, *, \
                      allow_no_indices=default, expand_wildcards=default,\
                      ignore_indices=default, ignore_unavailable=default,\
                      operation_threading=default, recovery=default, \
                      snapshot=default, human=default)

      A :ref:`coroutine <coroutine>` that get a comprehensive status
      information of one or more indices.

      :arg index: A comma-separated list of index names; use `_all` or
             empty string to perform the operation on all indices
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows
             to ignore `missing` ones, default u'none'
      :arg ignore_unavailable: Whether specified concrete indices
             should be ignored when unavailable (missing or closed)
      :arg operation_threading: TODO: ?
      :arg recovery: Return information about shard recovery
      :arg snapshot: For snapshot status set it to true
      :arg human: Whether to return time and byte values in human-readable
             format.

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-status.html>`_

   .. method:: stats(index=None, *, metric=default, \
                     completion_fields=default, docs=default, \
                     fielddata_fields=default, fields=default, \
                     groups=default, allow_no_indices=default, \
                     expand_wildcards=default, ignore_indices=default,\
                     ignore_unavailable=default, human=default, \
                     level=default, types=default)

      A :ref:`coroutine <coroutine>` that retrieve statistics on different
      operations happening on an index.

      :arg index: A comma-separated list of index names; use `_all` or
             empty string to perform the operation on all indices
      :arg metric: A comma-separated list of metrics to display. Possible
             values: "_all", "completion", "docs", "fielddata",
             "filter_cache", "flush", "get", "id_cache", "indexing", "merge",
             "percolate", "refresh", "search", "segments", "store", "warmer"
      :arg completion_fields: A comma-separated list of fields for
             `completion` metric (supports wildcards)
      :arg docs: the number of docs / deleted docs (docs not yet merged
             out). Note, affected by refreshing the index
      :arg fielddata_fields: A comma-separated list of fields for
             `fielddata` metric (supports wildcards)
      :arg fields: A comma-separated list of fields for `fielddata` and
             `completion` metric (supports wildcards)
      :arg groups: A comma-separated list of search groups for `search`
             statistics
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows
             to ignore `missing` ones (default: none)
      :arg ignore_unavailable: Whether specified concrete indices should
             be ignored when unavailable (missing or closed)
      :arg human: Whether to return time and byte values in human-readable
             format.
      :arg level: Return stats aggregated at cluster, index or shard level.
             ("cluster", "indices" or "shards", default: "indices")
      :arg types: A comma-separated list of document types for the
               `indexing` index metric

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-stats.html>`_

   .. method:: segments(index=None, *, \
                        allow_no_indices=default, expand_wildcards=default,\
                        ignore_indices=default, ignore_unavailable=default,\
                        human=default)

      A :ref:`coroutine <coroutine>` that provide low level segments
      information that a Lucene index (shard level) is built with.

      :arg index: A comma-separated list of index names; use `_all` or
             empty string to perform the operation on all indices
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows to
             ignore `missing` ones, default u'none'
      :arg ignore_unavailable: Whether specified concrete indices should
             be ignored when unavailable (missing or closed)
      :arg human: Whether to return time and byte values in human-readable
             format (default: false)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-segments.html>`_

   .. method:: optimize(index=None, *, \
                 flush=default, allow_no_indices=default, \
                 expand_wildcards=default, ignore_indices=default, \
                 ignore_unavailable=default, max_num_segments=default, \
                 only_expunge_deletes=default, operation_threading=default,\
                 wait_for_merge=default, force=default)

      A :ref:`coroutine <coroutine>` that explicitly optimize one or more
      indices through an API.

      :arg index: A comma-separated list of index names; use `_all` or
             empty string to perform the operation on all indices
      :arg flush: Specify whether the index should be flushed after
              performing the operation (default: true)
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows to
             ignore `missing` ones, default u'none'
      :arg ignore_unavailable: Whether specified concrete indices should
             be ignored when unavailable (missing or closed)
      :arg max_num_segments: The number of segments the index should be
             merged into (default: dynamic)
      :arg only_expunge_deletes: Specify whether the operation should only
             expunge deleted documents
      :arg operation_threading: TODO: ?
      :arg wait_for_merge: Specify whether the request should block until
             the merge process is finished (default: true)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-optimize.html>`_

   .. method:: recovery(index=None, *, \
                        active_only=default, detailed=default, human=default)

      A :ref:`coroutine <coroutine>` that provides insight into on-going shard
      recoveries. Recovery status may be reported for specific indices, or
      cluster-wide..

      :arg index: A comma-separated list of index names; use `_all` or
             empty string to perform the operation on all indices
      :arg active_only: Display only those recoveries that are currently
             on-going (default: 'false')
      :arg detailed: Whether to display detailed information about shard
             recovery (default: 'false')
      :arg human: Whether to return time and byte values in human-readable
             format. (default: 'false')

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/indices-recovery.html>`_

   .. method:: clear_cache(index=None, *, \
                           field_data=default, fielddata=default, \
                           fields=default, filter=default, \
                           filter_cache=default, filter_keys=default,\
                           id=default, id_cache=default, \
                           allow_no_indices=default, expand_wildcards=default,\
                           ignore_indices=default, ignore_unavailable=default,\
                           recycler=default)

      A :ref:`coroutine <coroutine>` that clear either all caches or
      specific cached associated with one or more indices.

      :arg index: A comma-separated list of index name to limit the
             operation
      :arg field_data: Clear field data
      :arg fielddata: Clear field data
      :arg fields: A comma-separated list of fields to clear when using the
             `field_data` parameter (default: all)
      :arg filter: Clear filter caches
      :arg filter_cache: Clear filter caches
      :arg filter_keys: A comma-separated list of keys to clear when using
             the `filter_cache` parameter (default: all)
      :arg id: Clear ID caches for parent/child
      :arg id_cache: Clear ID caches for parent/child
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows to
             ignore `missing` ones (default: none)
      :arg ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :arg index: A comma-separated list of index name to limit the
             operation
      :arg recycler: Clear the recycler cache

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-clearcache.html>`_

   .. method:: validate_query(index=None, doc_type=None, body=None, *, \
                       explain=default, allow_no_indices=default,\
                       expand_wildcards=default, ignore_indices=default,\
                       ignore_unavailable=default,\
                       operation_threading=default,\
                       q=default, source=default)

      A :ref:`coroutine <coroutine>` that validate a potentially expensive
      query without executing it.

      :arg index: A comma-separated list of index names to restrict the
             operation; use `_all` or empty string to perform the operation
             on all indices
      :arg doc_type: A comma-separated list of document types to restrict
             the operation; leave empty to perform the operation on all types
      :arg body: The query definition
      :arg explain: Return detailed information about the error
      :arg allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes
             `_all` string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
             concrete indices that are open, closed or both.
      :arg ignore_indices: When performed on multiple indices, allows to
             ignore `missing` ones (default: none)
      :arg ignore_unavailable: Whether specified concrete indices should
             be ignored when unavailable (missing or closed)
      :arg operation_threading: TODO: ?
      :arg q: Query in the Lucene query string syntax
      :arg source: The URL-encoded query definition (instead of using the
             request body)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-validate.html>`_

   .. method:: put_mapping(index, doc_type, body, *, \
                           allow_no_indices=default, expand_wildcards=default, \
                           ignore_conflicts=default, \
                           ignore_unavailable=default, \
                           master_timeout=default, timeout=default)

      A :ref:`coroutine <coroutine>` that registers specific mapping
      definition for a specific type.

      :arg index: A comma-separated list of index names the alias should
          point to (supports wildcards); use `_all` or omit to perform the
          operation on all indices.
      :arg doc_type: The name of the document type
      :arg body: The mapping definition
      :arg allow_no_indices: Whether to ignore if a wildcard indices
          expression resolves into no concrete indices. (This includes `_all`
          string or when no indices have been specified)
      :arg expand_wildcards: Whether to expand wildcard expression to concrete
          indices that are open, closed or both., default u'open'
      :arg ignore_conflicts: Specify whether to ignore conflicts while
          updating the mapping (default: false)
      :arg ignore_unavailable: Whether specified concrete indices should be
          ignored when unavailable (missing or closed)
      :arg master_timeout: Specify timeout for connection to master
      :arg timeout: Explicit operation timeout

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-put-mapping.html>`_

   .. method:: get_mapping(index, doc_type=None, *, \
                           ignore_unavailable=default, \
                           allow_no_indices=default, \
                           expand_wildcards=default, local=default)

      A :ref:`coroutine <coroutine>` that retrieves mapping
      definition of index or index/type.

      :arg index: A comma-separated list of index names; use `_all` or
            empty string for all indices
      :arg doc_type: A comma-separated list of document types
      :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This
            includes `_all` string or when no indices have been
            specified)
      :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.
      :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
      :arg local: Return local information, do not retrieve the state from
            master node (default: false)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-get-mapping.html>`_

   .. method:: delete_mapping(index, doc_type, *, \
                              master_timeout=default)

      A :ref:`coroutine <coroutine>` that deletes a mapping (type)
      along with its data

      :arg index: A comma-separated list of index names (supports wildcard);
            use `_all` for all indices
      :arg doc_type: A comma-separated list of document types to delete
            (supports wildcards); use `_all` to delete all document types in the
            specified indices.
      :arg master_timeout: Specify timeout for connection to master

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-delete-mapping.html>`_

   .. method:: get_field_mapping(field, index=None, doc_type=None, *, \
                                 include_defaults=default, ignore_unavailable=default, \
                                 allow_no_indices=default, expand_wildcards=default, \
                                 local=default)

      A :ref:`coroutine <coroutine>` that retrieves mapping definition of a specific field

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

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-get-field-mapping.html>`_

   .. method:: put_alias(name, index=None, body=None, *, \
                         timeout=default, master_timeout=default)

      A :ref:`coroutine <coroutine>` that creates an alias for a specific index/indices

      :arg index: A comma-separated list of index names the alias should
          point to (supports wildcards); use `_all` or omit to perform the
          operation on all indices.
      :arg name: The name of the alias to be created or updated
      :arg body: The settings for the alias, such as `routing` or `filter`
      :arg master_timeout: Specify timeout for connection to master
      :arg timeout: Explicit timestamp for the document

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

   .. method:: exists_alias(name, index=None, *, allow_no_indices=default, \
                            expand_wildcards=default, ignore_indices=default, \
                            ignore_unavailable=default, local=default)

      A :ref:`coroutine <coroutine>` that returns a boolean indicating whether given alias exists

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

      :returns: resulting boolean

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

   .. method:: get_alias(index=None, name=None, *, allow_no_indices=default, \
                         expand_wildcards=default, ignore_indices=default, \
                         ignore_unavailable=default, local=default)

      A :ref:`coroutine <coroutine>` that retrieves a specified alias.

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

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

   .. method:: get_aliases(index=None, name=None, *, local=default, \
                           timeout=default)

      A :ref:`coroutine <coroutine>` that retrieves a specified aliases.

      :arg index: A comma-separated list of index names to filter aliases
      :arg name: A comma-separated list of alias names to filter
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg timeout: Explicit operation timeout

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

   .. method:: update_aliases(body, *, timeout=default, \
                              master_timeout=default)

      A :ref:`coroutine <coroutine>` that updates a specified aliases.

      :arg body: The definition of `actions` to perform
      :arg master_timeout: Specify timeout for connection to master
      :arg timeout: Request timeout

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

   .. method:: delete_alias(index, name, *, timeout=default, \
                            master_timeout=default)

      A :ref:`coroutine <coroutine>` that deletes a specified aliases.

      :arg index: A comma-separated list of index names (supports wildcards);
          use `_all` for all indices
      :arg name: A comma-separated list of aliases to delete (supports
          wildcards); use `_all` to delete all aliases for the
          specified indices.
      :arg master_timeout: Specify timeout for connection to master
      :arg timeout: Explicit timestamp for the document

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-aliases.html>`_

   .. method:: put_template(name, body, *, create=default, order=default, \
                            timeout=default, master_timeout=default, \
                            flat_settings=default)

      A :ref:`coroutine <coroutine>` that creates an index template that will
      be automatically applied to new indices created.

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

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-templates.html>`_

   .. method:: exists_template(name, *, local=default)

      A :ref:`coroutine <coroutine>` that returns a boolean indicating whether
      given template exists.

      :arg name: The name of the template
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-templates.html>`_

   .. method:: get_template(name=None, *, flat_settings=default, \
                            local=default)

      A :ref:`coroutine <coroutine>` that retrieves an index template by its name.

      :arg name: The name of the template
      :arg flat_settings: Return settings in flat format (default: false)
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-templates.html>`_

   .. method:: delete_template(name, *, timeout=default, \
                               master_timeout=default)

      A :ref:`coroutine <coroutine>` that deletes an index template by its name.

      :arg name: The name of the template
      :arg master_timeout: Specify timeout for connection to master
      :arg timeout: Explicit operation timeout

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-templates.html>`_

   .. method:: put_warmer(name, body, index=None, doc_type=None, *, \
                          allow_no_indices=default, expand_wildcards=default, \
                          ignore_unavailable=default, master_timeout=default)

      A :ref:`coroutine <coroutine>` that create an index warmer to run
      registered search requests to warm up the index before it is available for search.

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

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-warmers.html>`_

   .. method:: get_warmer(index=None, doc_type=None, name=None, *, \
                          allow_no_indices=default, expand_wildcards=default, \
                          ignore_unavailable=default, local=default)

      A :ref:`coroutine <coroutine>` that retreieves an index warmer.

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

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-warmers.html>`_

   .. method:: delete_warmer(index, name, *, master_timeout=default)

      A :ref:`coroutine <coroutine>` that deletes an index warmer.

      :arg index: A comma-separated list of index names to delete
          warmers from (supports wildcards); use `_all` to perform
          the operation on all indices.
      :arg name: A comma-separated list of warmer names to delete (supports
          wildcards); use `_all` to delete all warmers in the
          specified indices.
      :arg master_timeout: Specify timeout for connection to master

      :returns: resulting JSON

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/indices-warmers.html>`_

CatClient
-----------------


.. class:: aioes.client.CatClient

   Class for retrieving elasticsearch information in human-readable way.

   .. method:: aliases(*, name=default, h=default, help=default, \
               local=default, master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that returns an info about aliases.

      :arg name: A comma-separated list of alias names to return
      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for connection to master
          node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cat-alias.html>`_


   .. method:: allocation(node_id=None, *, h=default, help=default, \
               local=default, master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that returns a snapshot of how
      shards have located around the cluster and the state of disk
      usage.

      :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information
      :arg bytes: The unit in which to display byte values
      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default ``False``
      :arg local: Return local information, do not retrieve the state from
            master node (default: ``False``)
      :arg master_timeout: Explicit operation timeout for connection
            to master node
      :arg v: Verbose mode. Display column headers, default ``False``

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cat-allocation.html>`_

   .. method:: count(index=None, *, h=default, help=default, \
               local=default, master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that returns an info about aliases.

      :arg index: A comma-separated list of index names to limit the returned
          information
      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for connection to
          master node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cat-count.html>`_

   .. method:: health(*, h=default, help=default, local=default, \
               master_timeout=default, ts=default, v=default)

      A :ref:`coroutine <coroutine>` that returns a health, which is a terse,
      one-line representation of the same information from
      :meth:`~elasticsearch.client.cluster.ClusterClient.health` API

      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for connection to master
          node
      :arg ts: Set to false to disable timestamping, default True
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-health.html>`_

   .. method:: help(*, help=default)

      A :ref:`coroutine <coroutine>` that returns help banner.

      :arg help: Return help information, default ``False``.

      :returns: help text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cat.html>`_

   .. method:: indices(self, index=None, *, bytes=default, h=default, help=default, \
               local=default, master_timeout=default, pri=default, v=default)

      A :ref:`coroutine <coroutine>` that returns a cross-section of each index

      :arg index: A comma-separated list of index names to limit the returned
          information
      :arg bytes: The unit in which to display byte values
      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for connection to
          master node
      :arg pri: Set to true to return stats only for primary shards, default
          False
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-indices.html>`_

   .. method:: master(*, h=default, help=default, local=default, \
               master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that displays the master's node ID,
      bound IP address, and node name

      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for connection to
          master node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-master.html>`_

   .. method:: nodes(*, h=default, help=default, local=default, \
              master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that shows the cluster topology.

      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for master connection
          node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-nodes.html>`_

   .. method:: recovery(index=None, *, bytes=default, h=default, help=default, \
                        local=default, master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that shows the view of shard replication.

      :arg index: A comma-separated list of index names to limit the returned
            information
      :arg bytes: The unit in which to display byte values
      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for master connection
          node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-recovery.html>`_

   .. method:: shards(index=None, *, h=default, help=default, local=default, \
                      master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that shows the detailed view of what nodes
      contain which shards.

      :arg index: A comma-separated list of index names to limit the returned
            information
      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for master connection
          node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-shards.html>`_

   .. method:: segments(index=None, *, h=default, help=default, local=default, \
                        master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that shows the detailed
      view of Lucene segments per index

      :arg index: A comma-separated list of index names to limit the returned
            information
      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for master connection
          node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-segments.html>`_

   .. method:: pending_tasks(*, h=default, help=default, local=default, \
                             master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that provides the same information as the
      :meth:`~elasticsearch.client.cluster.ClusterClient.pending_tasks` API
      in a convenient tabular format.

      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for master connection
          node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-pending-tasks.html>`_

   .. method:: thread_pool(*, full_id=default, h=default, help=default, \
                           local=default, master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that provides information about thread pools.

      :arg full_id: Enables displaying the complete node ids (default:false)
      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for master connection
          node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-thread-pool.html>`_

   .. method:: fielddata(*, fields=default, bytes=default, h=default, \
                         help=default, local=default, master_timeout=default, \
                         v=default)

      A :ref:`coroutine <coroutine>` that provides information about
      currently loaded fielddata on a per-node basis

      :arg fields: A comma-separated list of fields to return the fielddata
          size
      :arg bytes: The unit in which to display byte values
      :arg h: Comma-separated list of column names to display
      :arg help: Return help information (default: 'false')
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for master connection
          node
      :arg v: Verbose mode. Display column headers (default: 'false')

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-fielddata.html>`_

   .. method:: plugins(*, h=default, help=default, local=default, \
                       master_timeout=default, v=default)

      A :ref:`coroutine <coroutine>` that provides information about plugins.

      :arg h: Comma-separated list of column names to display
      :arg help: Return help information, default False
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)
      :arg master_timeout: Explicit operation timeout for master connection
          node
      :arg v: Verbose mode. Display column headers, default False

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-plugins.html>`_


ClusterClient
-----------------


.. class:: aioes.client.ClusterClient

   Class for retrieving elasticsearch information in human-readable way.

   .. method:: health(index=None, *, \
               level=default, local=default, master_timeout=default, \
               timeout=default, wait_for_active_shards=default, \
               wait_for_nodes=default, wait_for_relocating_shards=default, \
               wait_for_status=default)

      A :ref:`coroutine <coroutine>` that returns a very simple status on the health of the cluster.

      :arg index: Limit the information returned to a specific index
      :arg level: Specify the level of detail for returned information,
           default u'cluster'
      :arg local: Return local information, do not retrieve the state from
           master node (default: false)
      :arg master_timeout: Explicit operation timeout for connection to
           master node
      :arg timeout: Explicit operation timeout
      :arg wait_for_active_shards: Wait until the specified number of shards
           is active
      :arg wait_for_nodes: Wait until the specified number of nodes is
           available
      :arg wait_for_relocating_shards: Wait until the specified number of
           relocating shards is finished
      :arg wait_for_status: Wait until cluster is in a specific state,
           default None

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-health.html>`_

   .. method:: pending_tasks(*, local=default, master_timeout=default)

      A :ref:`coroutine <coroutine>` that returns a list of any cluster-level
      changes (e.g. create index, update mapping, allocate or fail shard)
      which have not yet been executed.

      :arg local: Return local information, do not retrieve the state
            from master node (default: false)
      :arg master_timeout: Specify timeout for connection to master

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-pending.html>`_

   .. method:: state(metric=None, index=None, *, index_templates=default, \
               local=default, master_timeout=default, flat_settings=default)

      A :ref:`coroutine <coroutine>` that returns a comprehensive state information of the whole cluster.

      :arg metric: Limit the information returned to the specified metrics.
          Possible values: "_all", "blocks", "index_templates", "metadata",
          "nodes", "routing_table", "master_node", "version"
      :arg index: A comma-separated list of index names; use `_all` or empty
          string to perform the operation on all indices
      :arg index_templates: A comma separated list to return specific index
          templates when returning metadata.
      :arg local: Return local information, do not retrieve the state
          from master node (default: false)
      :arg master_timeout: Specify timeout for connection to master
      :arg flat_settings: Return settings in flat format (default: false)

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-state.html>`_

   .. method:: stats(node_id=None, *, flat_settings=default, human=default)

      A :ref:`coroutine <coroutine>` that returns statistics from a cluster wide
      perspective. The API returns basic index metrics and information about
      the current nodes that form the cluster.

      :arg node_id: A comma-separated list of node IDs or names to limit the
          returned information; use `_local` to return information from the
          node you're connecting to, leave empty to get information from
          all nodes
      :arg flat_settings: Return settings in flat format (default: false)
      :arg human: Whether to return time and byte values in
          human-readable format.

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-stats.html>`_

   .. method:: reroute(body=None, *, dry_run=default, explain=default, \
               filter_metadata=default, master_timeout=default, \
               timeout=default)

      A :ref:`coroutine <coroutine>` that executes a cluster reroute
      allocation command including specific commands.

      :arg body: The definition of `commands` to perform
          (`move`, `cancel`, `allocate`)
      :arg dry_run: Simulate the operation only and return
          the resulting state
      :arg explain: Return an explanation of why the commands can or
          cannot be executed
      :arg filter_metadata: Don't return cluster state metadata
          (default: false)
      :arg master_timeout: Explicit operation timeout for connection
          to master node
      :arg timeout: Explicit operation timeout

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-reroute.html>`_

   .. method:: get_settings(*, flat_settings=default, master_timeout=default, \
               timeout=default)

      A :ref:`coroutine <coroutine>` that returns cluster settings.

      :arg flat_settings: Return settings in flat format (default: false)
      :arg master_timeout: Explicit operation timeout for connection
          to master node
      :arg timeout: Explicit operation timeout

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-update-settings.html>`_

   .. method:: put_settings(body, *, flat_settings=default)

      A :ref:`coroutine <coroutine>` that updates cluster settings.

      :arg body: The settings to be updated. Can be either `transient` or
          `persistent` (survives cluster restart).
      :arg flat_settings: Return settings in flat format (default: false)

      :returns: resulting text

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-update-settings.html>`_

NodesClient
-----------------


.. class:: aioes.client.NodesClient

   Class for getting information about elasticsearch nodes.

   .. method:: info(node_id=None, metric=None, *, \
                    flat_settings=default, human=default)

      A :ref:`coroutine <coroutine>` that retrieves one or more (or all)
      of the cluster nodes information.

      :arg node_id: A comma-separated list of node IDs or names to limit the
          returned information; use ``"_local"`` to return information from the
          node you're connecting to, leave empty to get information from all
          nodes
      :arg metric: A comma-separated list of metrics you wish
          returned. Leave empty to return all. Choices are
          ``"settings"``, ``"os"``, ``"process"``, ``"jvm"``,
          ``"thread_pool"``, ``"network"``, ``"transport"``,
          ``"http"``, ``"plugin"``
      :arg flat_settings: Return settings in flat format (default: ``False``)
      :arg human: Whether to return time and byte values in human-readable
          format, default ``False``

      :returns: resulting info

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-nodes-info.html>`_

   .. method:: shutdown(node_id=None, *, delay=default, exit=default)

      A :ref:`coroutine <coroutine>` that shutdowns one or more (or all) nodes in
      the cluster.

      :arg node_id: A comma-separated list of node IDs or names to perform
          the operation on; use `_local` to perform the operation on
          the node you're connected to, leave empty to perform the operation
          on all nodes
      :arg delay: Set the delay for the operation (default: 1s)
      :arg exit: Exit the JVM as well (default: true)

      :returns: resulting info

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-nodes-shutdown.html>`_

   .. method:: stats(node_id=None, metric=None, index_metric=None, *, \
                     completion_fields=default, fielddata_fields=default, \
                     fields=default, groups=default, human=default, level=default, \
                     types=default)

      A :ref:`coroutine <coroutine>` that allows to retrieve one or more (or all) of
      the cluster nodes statistics.

      :arg node_id: A comma-separated list of node IDs or names to limit the
          returned information; use `_local` to return information from the
          node you're connecting to, leave empty to get information from all
          nodes
      :arg metric: Limit the information returned to the specified metrics.
          Possible options are: "_all", "breaker", "fs", "http", "indices",
          "jvm", "network", "os", "process", "thread_pool", "transport"
      :arg index_metric: Limit the information returned for `indices` metric
          to the specific index metrics. Isn't used if `indices` (or `all`)
          metric isn't specified. Possible options are: "_all", "completion",
          "docs", "fielddata", "filter_cache", "flush", "get", "id_cache",
          "indexing", "merge", "percolate", "refresh", "search", "segments",
          "store", "warmer"
      :arg completion_fields: A comma-separated list of fields
          for `fielddata` and `suggest` index metric (supports wildcards)
      :arg fielddata_fields: A comma-separated list of fields for `fielddata`
          index metric (supports wildcards)
      :arg fields: A comma-separated list of fields for `fielddata` and
          `completion` index metric (supports wildcards)
      :arg groups: A comma-separated list of search groups for `search` index
          metric
      :arg human: Whether to return time and byte values in human-readable
          format., default False
      :arg level: Return indices stats aggregated at node, index or shard
          level, default 'node'
      :arg types: A comma-separated list of document types for the `indexing`
          index metric

      :returns: resulting info

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-nodes-stats.html>`_

   .. method:: hot_threads(node_id=None, *, type_=default, interval=default, \
                           snapshots=default, threads=default)

      A :ref:`coroutine <coroutine>` that allows to get the current hot threads on each node
      in the cluster.

      :arg node_id: A comma-separated list of node IDs or names to limit the
          returned information; use `_local` to return information from the
          node you're connecting to, leave empty to get information from all
          nodes
      :arg type_: The type to sample (default: cpu)
      :arg interval: The interval for the second sampling of threads
      :arg snapshots: Number of samples of thread stacktrace (default: 10)
      :arg threads: Specify the number of threads to provide information for
          (default: 3)

      :returns: resulting info

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-nodes-hot-threads.html>`_



SnapshotClient
-----------------


.. class:: aioes.client.SnapshotClient

   Class for manipulating elasticsearch snapshots.

   .. method:: create(repository, snapshot, body=None, *, \
               master_timeout=default, wait_for_completion=default)

      A :ref:`coroutine <coroutine>` that creates a snapshot in repository

      :arg repository: A repository name
      :arg snapshot: A snapshot name
      :arg body: The snapshot definition
      :arg master_timeout: Explicit operation timeout for connection
          to master node
      :arg wait_for_completion: Should this request wait until
          the operation has completed before returning, default False

      :returns: resulting info.

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

   .. method:: delete(repository, snapshot, *, master_timeout=default)

      A :ref:`coroutine <coroutine>` that deletes a snapshot in repository

      :arg repository: A repository name
      :arg snapshot: A snapshot name
      :arg master_timeout: Explicit operation timeout for connection
          to master node

      :returns: resulting info.

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

   .. method:: get(repository, snapshot, *, master_timeout=default)

      A :ref:`coroutine <coroutine>` that retrieves information about a snapshot.

      :arg repository: A comma-separated list of repository names
      :arg snapshot: A comma-separated list of snapshot names
      :arg master_timeout: Explicit operation timeout for connection
          to master node

      :returns: resulting info.

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

   .. method:: delete_repository(repository, *, master_timeout=default, \
                                 timeout=default)

      A :ref:`coroutine <coroutine>` that removes a shared file system repository.

      :arg repository: A comma-separated list of repository names
      :arg snapshot: A comma-separated list of snapshot names
      :arg master_timeout: Explicit operation timeout for connection
          to master node

      :returns: resulting info.

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

   .. method:: get_repository(repository=None, *, local=default, \
                              master_timeout=default)

      A :ref:`coroutine <coroutine>` that returns information about registered repositories.

      :arg repository: A comma-separated list of repository names
      :arg master_timeout: Explicit operation timeout for connection
          to master node
      :arg local: Return local information, do not retrieve the state from
          master node (default: false)

      :returns: resulting info.

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

   .. method:: create_repository(repository, body, *, master_timeout=default, \
                                 timeout=default)

      A :ref:`coroutine <coroutine>` that registers a shared file system repository.

      :arg repository: A repository name
      :arg body: The repository definition
      :arg master_timeout: Explicit operation timeout for connection
          to master node
      :arg timeout: Explicit operation timeout

      :returns: resulting info.

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

   .. method:: restore(repository, snapshot, body=None, *, \
                       master_timeout=default, wait_for_completion=default)

      A :ref:`coroutine <coroutine>` that restores a snapshot.

      :arg repository: A repository name
      :arg snapshot: A snapshot name
      :arg body: Details of what to restore
      :arg master_timeout: Explicit operation timeout for connection
          to master node
      :arg wait_for_completion: Should this request wait until the operation
          has completed before returning, default False

      :returns: resulting info.

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

   .. method:: status(repository=None, snapshot=None, *, \
               master_timeout=default)

      A :ref:`coroutine <coroutine>` that returns snapshot status info.

      :arg repository: A repository name
      :arg snapshot: A comma-separated list of snapshot names
      :arg master_timeout: Explicit operation timeout for connection to master
            node

      :returns: resulting snapshot info.

      .. Seealso::

         `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html#_snapshot_status>`_
