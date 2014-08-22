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

      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
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
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_


   .. method:: clear_scroll(scroll_id=None, body=None, *, pretty=default,\
                            format=default)

      A :ref:`coroutine <coroutine>` that clear the scroll request created
      by specifying the scroll parameter to search.

      :param scroll_id: The scroll ID or a list of scroll IDs
      :param body: A comma-separated list of scroll IDs to clear if none was
             specified via the scroll_id parameter
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_


   .. method:: delete(index, doc_type, id, *, consistency=default, \
                      parent=default, refresh=default,\
                      replication=default, routing=default, \
                      timeout=default, version=default, \
                      version_type=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that delete a typed JSON document from
      a specific index based on its id.

      :param index: The name of the index
      :param doc_type: The type of the document
      :param id: The document ID
      :param consistency: Specific write consistency setting for the operation
      :param parent: ID of parent document
      :param refresh: Refresh the index after performing the operation
      :param replication: Specific replication type (default: sync)
      :param routing: Specific routing value
      :param timeout: Explicit operation timeout
      :param version: Explicit version number for concurrency control
      :param version_type: Specific version type
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-delete.html>`_


   .. method:: count(index=None, doc_type=None, body=None, *, \
                     allow_no_indices=default, expand_wildcards=default,\
                     ignore_unavailable=default, min_score=default,\
                     preference=default, q=default, routing=default,
                     source=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that execute a query and get the 
      number of matches for that query.

      :param index: A comma-separated list of indices to restrict the results
      :param doc_type: A comma-separated list of types to restrict the results
      :param body: A query to restrict the results (optional)
      :param allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :param expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :param ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :param min_score: Include only documents with a specific `_score` value 
             in the result
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param q: Query in the Lucene query string syntax
      :param routing: Specific routing value
      :param source: The URL-encoded query definition (instead of using the request body)
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-count.html>`_


   .. method:: bulk(body, index=None, doc_type=None, *, consistency=default,\
                    refresh=default, routing=default, replication=default, \
                    timeout=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that perform many index/delete 
      operations in a single API call.

      :param body: The operation definition and data (action-data pairs), as
             either a newline separated string, or a sequence of dicts to
             serialize (one per row).
      :param index: Default index for items which don't provide one
      :param doc_type: Default document type for items which don't provide one
      :param consistency: Explicit write consistency setting for the operation
      :param refresh: Refresh the index after performing the operation
      :param routing: Specific routing value
      :param replication: Explicitly set the replication type (default: sync)
      :param timeout: Explicit operation timeout
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-bulk.html>`_


   .. method:: msearch(body, index=None, doc_type=None, *, \
                       search_type=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that executes several search requests
      within the same API.

      :param body: The request definitions (metadata-search request definition
             pairs), as either a newline separated string, or a sequence of
             dicts to serialize (one per row).
      :param index: A comma-separated list of index names to use as default
      :param doc_type: A comma-separated list of document types to use as default
      :param search_type: Search operation type
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-multi-search.html>`_


   .. method:: delete_by_query(index, doc_type=None, body=None, *, \
                               allow_no_indices=default, analyzer=default, \
                               consistency=default, default_operator=default,\
                               df=default, expand_wildcards=default, \
                               ignore_unavailable=default, q=default, \
                               replication=default, routing=default, \
                               source=default, timeout=default, pretty=default, \
                               format=default)

      A :ref:`coroutine <coroutine>` that delete documents from one or more 
      indices and one or more types based on a query.

      :param index: A comma-separated list of indices to restrict the operation;
             use `_all` to perform the operation on all indices
      :param doc_type: A comma-separated list of types to restrict the operation
      :param body: A query to restrict the operation specified with the Query
             DSL
      :param allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :param analyzer: The analyzer to use for the query string
      :param consistency: Specific write consistency setting for the operation
      :param default_operator: The default operator for query string query (AND
             or OR), default u'OR'
      :param df: The field to use as default where no field prefix is given in
             the query string
      :param expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default u'open'
      :param ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :param q: Query in the Lucene query string syntax
      :param replication: Specific replication type, default u'sync'
      :param routing: Specific routing value
      :param source: The URL-encoded query definition (instead of using the
             request body)
      :param timeout: Explicit operation timeout
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-delete-by-query.html>`_



   .. method:: suggest(body, index=None, *, allow_no_indices=default, \
                       expand_wildcards=default, ignore_unavailable=default,\
                       preference=default, routing=default, source, \
                       pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that suggests similar looking terms based on a provided
      text by using a suggester.

      :param index: A comma-separated list of index names to restrict the operation;
             use `_all` or empty string to perform the operation on all indices
      :param body: The request definition
      :param allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :param expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :param ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param routing: Specific routing value
      :param source: The URL-encoded request definition (instead of using request body)
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-search.html>`_


   .. method:: percolate(index, doc_type, id=None, body=None, *, \
                         allow_no_indices=default, expand_wildcards=default,\
                         ignore_unavailable=default, percolate_format=default,\
                         percolate_index=default, percolate_type=default,\
                         preference=default, routing=default, version=default,\
                         version_type=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that allows to register queries against 
      an index, and then send percolate requests which include a doc, and getting 
      back the queries that match on that doc out of the set of registered queries.

      :param index: The index of the document being percolated.
      :param doc_type: The type of the document being percolated.
      :param id: Substitute the document in the request body with a document
             that is known by the specified id. On top of the id, the index and
             type parameter will be used to retrieve the document from within the
             cluster.
      :param body: The percolator request definition using the percolate DSL
      :param allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :param expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :param ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :param percolate_format: Return an array of matching query IDs instead of
             objects
      :param percolate_index: The index to percolate the document into. Defaults
             to index.
      :param percolate_type: The type to percolate document into. Defaults to
             type.
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param routing: A comma-separated list of specific routing values
      :param version: Explicit version number for concurrency control
      :param version_type: Specific version type
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_


   .. method:: mpercolate(body, index=None, doc_type=None, *, \
                          allow_no_indices=default, expand_wildcards=default, \
                          ignore_unavailable=default, pretty=default, \
                          format=default)

      A :ref:`coroutine <coroutine>` that allows to register queries against 
      an index, and then send percolate requests which include a doc, and getting
      back the queries that match on that doc out of the set of registered queries.

      :param index: The index of the document being count percolated to use as
             default
      :param doc_type: The type of the document being percolated to use as
             default.
      :param body: The percolate request definitions (header & body pair),
             separated by newlines
      :param allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :param expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :param ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

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
                               version_type=default, pretty=default, \
                               format=default)

      A :ref:`coroutine <coroutine>` that allows to register queries against an 
      index, and then send percolate requests which include a doc, and getting back 
      the queries that match on that doc out of the set of registered queries.

      :param index: The index of the document being count percolated.
      :param doc_type: The type of the document being count percolated.
      :param id: Substitute the document in the request body with a document
             that is known by the specified id. On top of the id, the index and
             type parameter will be used to retrieve the document from within the
             cluster.
      :param body: The count percolator request definition using the percolate DSL
      :param allow_no_indices: Whether to ignore if a wildcard indices
             expression resolves into no concrete indices. (This includes `_all`
             string or when no indices have been specified)
      :param expand_wildcards: Whether to expand wildcard expression to concrete
             indices that are open, closed or both., default 'open'
      :param ignore_unavailable: Whether specified concrete indices should be
             ignored when unavailable (missing or closed)
      :param percolate_index: The index to count percolate the document into.
             Defaults to index.
      :param percolate_type: The type to count percolate document into. Defaults
             to type.
      :param preference: Specify the node or shard the operation should be
             performed on (default: random)
      :param routing: A comma-separated list of specific routing values
      :param version: Explicit version number for concurrency control
      :param version_type: Specific version type
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

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
                   search_type=default, search_types=default, stop_words=default,\
                   pretty=default, format=default)

      A :ref:`coroutine <coroutine>` which get documents that are "like" a specified document

      :param index: The name of the index
      :param doc_type: The type of the document (use `_all` to fetch the first
             document matching the ID across all types)
      :param id: The document ID
      :param body: A specific search request definition
      :param boost_terms: The boost factor
      :param include: Whether to include the queried document from the response
      :param max_doc_freq: The word occurrence frequency as count: words with
             higher occurrence in the corpus will be ignored
      :param max_query_terms: The maximum query terms to be included in the generated query
      :param max_word_length: The minimum length of the word: longer words will be ignored
      :param min_doc_freq: The word occurrence frequency as count: words with
             lower occurrence in the corpus will be ignored
      :param min_term_freq: The term frequency as percent: terms with lower
             occurence in the source document will be ignored
      :param min_word_length: The minimum length of the word: shorter words will be ignored
      :param mlt_fields: Specific fields to perform the query against
      :param percent_terms_to_match: How many terms have to match in order to
             consider the document a match (default: 0.3)
      :param routing: Specific routing value
      :param search_from: The offset from which to return results
      :param search_indices: A comma-separated list of indices to perform the
             query against (default: the index containing the document)
      :param search_query_hint: The search query hint
      :param search_scroll: A scroll search request definition
      :param search_size: The number of documents to return (default: 10)
      :param search_source: A specific search request definition (instead of
             using the request body)
      :param search_type: Specific search type (eg. `dfs_then_fetch`, `count`, etc)
      :param search_types: A comma-separated list of types to perform the query
             against (default: the same type as the document)
      :param stop_words: A list of stop words to be ignored
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-more-like-this.html>`_


   .. method:: termvector(index, doc_type, id, body=None, *, \
                          field_statistics=default, fields=default, \
                          offsets=default, parent=default, payloads=default,\
                          positions=default, preference=default, routing=default,\
                          term_statistics=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that returns information and statistics on 
      terms in the fields of a particular document as stored in the index.

      :param index: The index in which the document resides.
      :param doc_type: The type of the document.
      :param id: The id of the document.
      :param body: Define parameters. See documentation.
      :param field_statistics: Specifies if document count, sum of document
             frequencies and sum of total term frequencies should be returned.
             (default True)
      :param fields: A comma-separated list of fields to return.
      :param offsets: Specifies if term offsets should be returned. (default True)
      :param parent: Parent id of documents.
      :param payloads: Specifies if term payloads should be returned. (default True)
      :param positions: Specifies if term positions should be returned. (default True)
      :param preference: Specify the node or shard the operation should be
             performed on (default: random).
      :param routing: Specific routing value.
      :param term_statistics: Specifies if total term frequency and document
             frequency should be returned., default False
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-termvectors.html>`_


   .. method:: mtermvectors(index=None, doc_type=None, body=None, *, \
                            field_statistics=default, fields=default,
                            ids=default, offsets=default, parent=default,
                            payloads=default, positions=default,
                            preference=default, routing=default,
                            term_statistics=default, pretty=default,
                            format=default)

      A :ref:`coroutine <coroutine>` allows to get multiple termvectors based on 
      an index, type and id.

      :param index: The index in which the document resides.
      :param doc_type: The type of the document.
      :param body: Define ids, parameters or a list of parameters per document
             here. You must at least provide a list of document ids. See
             documentation.
      :param field_statistics: Specifies if document count, sum of document
             frequencies and sum of total term frequencies should be returned.
             Applies to all returned documents unless otherwise specified in body
             "params" or "docs". (default True)
      :param fields: A comma-separated list of fields to return. Applies to all
             returned documents unless otherwise specified in body "params" or
             "docs".
      :param ids: A comma-separated list of documents ids. You must define ids
             as parameter or set "ids" or "docs" in the request body
      :param offsets: Specifies if term offsets should be returned. Applies to
             all returned documents unless otherwise specified in body "params"
             or "docs". (default True)
      :param parent: Parent id of documents. Applies to all returned documents
             unless otherwise specified in body "params" or "docs".
      :param payloads: Specifies if term payloads should be returned. Applies to
             all returned documents unless otherwise specified in body "params"
             or "docs". (default True)
      :param positions: Specifies if term positions should be returned. Applies
             to all returned documents unless otherwise specified in body
             "params" or "docs". (default True)
      :param preference: Specify the node or shard the operation should be
             performed on (default: random) .Applies to all returned documents
             unless otherwise specified in body "params" or "docs".
      :param routing: Specific routing value. Applies to all returned documents
             unless otherwise specified in body "params" or "docs".
      :param term_statistics: Specifies if total term frequency and document
             frequency should be returned. Applies to all returned documents
             unless otherwise specified in body "params" or "docs". (default
             False)
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-multi-termvectors.html>`_


   .. method:: benchmark(index=None, doc_type=None, body=None, *, \
                         verbose=default, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that provides a standard mechanism for 
      submitting queries and measuring their performance relative to one another.

      :param index: A comma-separated list of index names; use `_all` or empty
             string to perform the operation on all indices
      :param doc_type: The name of the document type
      :param body: The search definition using the Query DSL
      :param verbose: Specify whether to return verbose statistics about each
             iteration (default: false)
      :param pretty: the JSON returned will be pretty formatted (use it for debugging only!)
      :param format: Format of the output, default 'detailed'

      :returns: resulting JSON

      .. Seealso::

          `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-benchmark.html>`_
