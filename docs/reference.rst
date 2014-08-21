aioes reference
================

.. module:: aioes
   :synopsis: A library for accessing Elasticsearch server.
.. currentmodule:: aioes


Elasticsearch
-----------------


.. class:: Elasticsearch

   Class for operating on Elasticsearch cluster.

   .. method:: ping(*, pretty=default, format=default)

      A :ref:`coroutine <coroutine>` that returns True if the cluster is up,
      False otherwise.

      :param pretty:
      :param format: Format of the output, default 'detailed'

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
                      routing=default, pretty=default, format=default)

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
      :param pretty:
      :param format: Format of the output, default 'detailed'

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
      :param realtime: Specify whether to perform the operation in realtime or search mode
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
      :param realtime: Specify whether to perform the operation in realtime or search mode
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
