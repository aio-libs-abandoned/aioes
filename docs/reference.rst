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


   .. method:: info(*, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that returns basic info from the
      current cluster.

      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: bool


   .. method:: index(index, doc_type, body, id=None, *, \
                     consistency=default, op_type=default, parent=default, \
                     refresh=default, replication=default, routing=default, \
                     timeout=default, timestamp=default, ttl=default, \
                     version=default, version_type=default, pretty=default, \
                     format=default)

      A :ref:`coroutine <coroutine>` that adds or updates a typed JSON
      document in a specific index, making it searchable.

      :param index: The name of the index
      :param doc_type: The type of the document
      :param body: The document
      :param id: Document ID
      :param consistency: Explicit write consistency setting for the operation
      :param op_type: Explicit operation type (default: index)
      :param parent: ID of the parent document
      :param refresh: Refresh the index after performing the operation
      :param replication: Specific replication type (default: sync)
      :param routing: Specific routing value
      :param timeout: Explicit operation timeout
      :param timestamp: Explicit timestamp for the document
      :param ttl: Expiration time for the document
      :param version: Explicit version number for concurrency control
      :param version_type: Specific version type
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-index_.html>`_


   .. method:: create(index, doc_type, body, id=None, *, consistency=default, \
                      parent=default, percolate=default, refresh=default, \
                      replication=default, routing=default, timeout=default, \
                      timestamp=default, ttl=default, version=default, \
                      version_type=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that adds a typed JSON document in a
      specific index, making it searchable.
      Behind the scenes this method calls index(..., op_type='create')

      :param index: The name of the index
      :param doc_type: The type of the document
      :param id: Document ID
      :param body: The document
      :param consistency: Explicit write consistency setting for the operation
      :param id: Specific document ID (when the POST method is used)
      :param parent: ID of the parent document
      :param percolate: Percolator queries to execute while indexing the document
      :param refresh: Refresh the index after performing the operation
      :param replication: Specific replication type (default: sync)
      :param routing: Specific routing value
      :param timeout: Explicit operation timeout
      :param timestamp: Explicit timestamp for the document
      :param ttl: Expiration time for the document
      :param version: Explicit version number for concurrency control
      :param version_type: Specific version type
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: exists(index, id, doc_type='_all', *, parent=default, \
                      preference=default, realtime=default, refresh=default, \
                      routing=default)

      A :ref:`coroutine <coroutine>` that returns a boolean indicating
      whether or not given document exists in Elasticsearch.

      :param index: The name of the index
      :param id: The document ID
      :param doc_type: The type of the document (uses `_all` by default to
             fetch the first document matching the ID across all types)
      :param parent: The ID of the parent document
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param realtime: Specify whether to perform the operation in realtime or
             search mode
      :param refresh: Refresh the shard containing the document before
             performing the operation
      :param routing: Specific routing value

      :returns: bool

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: get(index, id, doc_type='_all', *, _source=default,\
                   _source_exclude=default, _source_include=default, \
                   fields=default, parent=default, preference=default, \
                   realtime=default, refresh=default, routing=default, \
                   version=default, version_type=default, pretty=default, \
                   format=default)

      A :ref:`coroutine <coroutine>` that get a typed JSON document from the
      index based on its id.

      :param index: The name of the index
      :param id: The document ID
      :param doc_type: The type of the document (uses `_all` by default to
             fetch the first document matching the ID across all types)
      :param _source: True or false to return the _source field or not, or a
             list of fields to return
      :param _source_exclude: A list of fields to exclude from the returned
             _source field
      :param _source_include: A list of fields to extract and return from the
             _source field
      :param fields: A comma-separated list of fields to return in the response
      :param parent: The ID of the parent document
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param realtime: Specify whether to perform the operation in realtime or
             search mode
      :param refresh: Refresh the shard containing the document before
             performing the operation
      :param routing: Specific routing value
      :param version: Explicit version number for concurrency control
      :param version_type: Explicit version number for concurrency control
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: mget(body, index=None, doc_type=None, *, _source=default, \
                    _source_exclude=default, _source_include=default, \
                    fields=default, parent=default, preference=default, \
                    realtime=default, refresh=default, routing=default, \
                    pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that get multiple documents based on an index, 
      type (optional) and ids.

      :param body: Document identifiers; can be either `docs` (containing full
             document information) or `ids` (when index and type is provided in the URL.
      :param index: The name of the index
      :param doc_type: The type of the document
      :param _source: True or false to return the _source field or not, or a
             list of fields to return
      :param _source_exclude: A list of fields to exclude from the returned
             _source field
      :param _source_include: A list of fields to extract and return from the
             _source field
      :param fields: A comma-separated list of fields to return in the response
      :param parent: The ID of the parent document
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param realtime: Specify whether to perform the operation in realtime or
             search mode
      :param refresh: Refresh the shard containing the document before
             performing the operation
      :param routing: Specific routing value
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: get_source(index, id, doc_type='_all', *, _source=default, \
                          _source_exclude=default, _source_include=default, \
                          parent=default, preference=default, realtime=default,\
                          refresh=default, routing=default, version=default, \
                          version_type=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that get the source of a document by it's 
      index, type and id.

      :param index: The name of the index
      :param doc_type: The type of the document (uses `_all` by default to
             fetch the first document matching the ID across all types)
      :param id: The document ID
      :param _source: True or false to return the _source field or not, or a
             list of fields to return
      :param _source_exclude: A list of fields to exclude from the returned
             _source field
      :param _source_include: A list of fields to extract and return from the
             _source field
      :param parent: The ID of the parent document
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param realtime: Specify whether to perform the operation in realtime
             or search mode
      :param refresh: Refresh the shard containing the document before
             performing the operation
      :param routing: Specific routing value
      :param version: Explicit version number for concurrency control
      :param version_type: Explicit version number for concurrency control
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_


   .. method:: update(index, doc_type, id, body=None, *, \
                      consistency=default, fields=default, lang=default,\
                      parent=default, refresh=default, \
                      replication=default, retry_on_conflict=default, \
                      routing=default, script=default, timeout=default,\
                      timestamp=default, ttl=default, version=default, \
                      version_type=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that update a document based on a script or partial data provided.

      :param index: The name of the index
      :param doc_type: The type of the document
      :param id: Document ID
      :param body: The request definition using either `script` or partial `doc`
      :param consistency: Explicit write consistency setting for the operation
      :param fields: A comma-separated list of fields to return in the response
      :param lang: The script language (default: mvel)
      :param parent: ID of the parent document
      :param refresh: Refresh the index after performing the operation
      :param replication: Specific replication type (default: sync)
      :param retry_on_conflict: Specify how many times should the operation be
             retried when a conflict occurs (default: 0)
      :param routing: Specific routing value
      :param script: The URL-encoded script definition (instead of using request body)
      :param timeout: Explicit operation timeout
      :param timestamp: Explicit timestamp for the document
      :param ttl: Expiration time for the document
      :param version: Explicit version number for concurrency control
      :param version_type: Explicit version number for concurrency control
      :param pretty:
      :param format: Format of the output, default 'detailed'

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
                      timeout=default, version=default, pretty=default, \
                      format=default)

      A :ref:`coroutine <coroutine>` that execute a search query and get back 
      search hits that match the query.

      :param index: A comma-separated list of index names to search; use `_all`
            or empty string to perform the operation on all indices
      :param doc_type: A comma-separated list of document types to search;
            leave empty to perform the operation on all types
      :param body: The search definition using the Query DSL
      :param _source: True or false to return the _source field or not, or a
            list of fields to return
      :param _source_exclude: A list of fields to exclude from the returned
            _source field
      :param _source_include: A list of fields to extract and return from the
            _source field
      :param analyze_wildcard: Specify whether wildcard and prefix queries
            should be analyzed (default: false)
      :param analyzer: The analyzer to use for the query string
      :param default_operator: The default operator for query string query (AND
            or OR) (default: OR)
      :param df: The field to use as default where no field prefix is given in
            the query string
      :param explain: Specify whether to return detailed information about
            score computation as part of a hit
      :param fields: A comma-separated list of fields to return as part of a hit
      :param indices_boost: Comma-separated list of index boosts
      :param lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
      :param allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
      :param expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
      :param ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
      :param lowercase_expanded_terms: Specify whether query terms should be lowercased
      :param from\_: Starting offset (default: 0)
      :param preference: Specify the node or shard the operation should be
            performed on (default: random)
      :param q: Query in the Lucene query string syntax
      :param routing: A comma-separated list of specific routing values
      :param scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
      :param search_type: Search operation type
      :param size: Number of hits to return (default: 10)
      :param sort: A comma-separated list of <field>:<direction> pairs
      :param source: The URL-encoded request definition using the Query DSL
            (instead of using request body)
      :param stats: Specific 'tag' of the request for logging and statistical purposes
      :param suggest_field: Specify which field to use for suggestions
      :param suggest_mode: Specify suggest mode (default: missing)
      :param suggest_size: How many suggestions to return in response
      :param suggest_text: The source text for which the suggestions should be returned
      :param timeout: Explicit operation timeout
      :param version: Specify whether to return document version as part of a hit
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-search.html>`_


   .. method:: search_shards(index=None, doc_type=None, *, \
                             allow_no_indices=default, \
                             expand_wildcards=default,\
                             ignore_unavailable=default, \
                             local=default, preference=default, \
                             routing=default, pretty=default, \
                             format=default)

      A :ref:`coroutine <coroutine>` that returns the indices and shards that a search
      request would be executed against. This can give useful feedback for working
      out issues or planning optimizations with routing and shard preferences
      execute a search query and get back search hits that match the query.

      :param index: The name of the index
      :param doc_type: The type of the document
      :param allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :param expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both. (default: '"open"')
      :param ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :param local: Return local information, do not retrieve the state from
             master node (default: false)
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param routing: Specific routing value
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-shards.html>`_


   .. method:: search_template(index=None, doc_type=None, body=None, *, \
                               allow_no_indices=default, \
                               expand_wildcards=default, \
                               ignore_unavailable=default, preference=default, \
                               routing=default, scroll=default, \
                               search_type=default, pretty=default, \
                               format=default)

      A :ref:`coroutine <coroutine>` that accepts a query template and a map of
      key/value pairs to fill in template parameters.

      :param index: A comma-separated list of index names to search; use `_all`
             or empty string to perform the operation on all indices
      :param doc_type: A comma-separated list of document types to search; leave
             empty to perform the operation on all types
      :param body: The search definition template and its params
      :param allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :param expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :param ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param routing: A comma-separated list of specific routing values
      :param scroll: Specify how long a consistent view of the index should be
             maintained for scrolled search
      :param search_type: Search operation type
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/query-dsl-template-query.html>`_


   .. method:: explain(index, doc_type, id, body=None, *, \
                       _source=default, _source_exclude=default, \
                       _source_include=default, analyze_wildcard=default,\
                       analyzer=default, default_operator=default, \
                       df=default, fields=default, lenient=default,\
                       lowercase_expanded_terms=default, parent=default,\
                       preference=default, q=default, routing=default,\
                       source=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that computes a score explanation for a 
      query and a specific document. This can give useful feedback whether a 
      document matches or didn't match a specific query.

      :param index: The name of the index
      :param doc_type: The type of the document
      :param id: The document ID
      :param body: The query definition using the Query DSL
      :param _source: True or false to return the _source field or not, or a
             list of fields to return
      :param _source_exclude: A list of fields to exclude from the returned
             _source field
      :param _source_include: A list of fields to extract and return from the
             _source field
      :param analyze_wildcard: Specify whether wildcards and prefix queries in
             the query string query should be analyzed (default: false)
      :param analyzer: The analyzer for the query string query
      :param default_operator: The default operator for query string query (AND
             or OR), (default: OR)
      :param df: The default field for query string query (default: _all)
      :param fields: A comma-separated list of fields to return in the response
      :param lenient: Specify whether format-based query failures (such as
             providing text to a numeric field) should be ignored
      :param lowercase_expanded_terms: Specify whether query terms should be lowercased
      :param parent: The ID of the parent document
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param q: Query in the Lucene query string syntax
      :param routing: Specific routing value
      :param source: The URL-encoded query definition (instead of using the
             request body)
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-explain.html>`_


   .. method:: scroll(scroll_id, *, scroll=default, pretty=default, \
                      format=default)

      A :ref:`coroutine <coroutine>` that scroll a search request created by 
      specifying the scroll parameter

      :param scroll_id: The scroll ID
      :param scroll: Specify how long a consistent view of the index should be
             maintained for scrolled search
      :param pretty:
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_
