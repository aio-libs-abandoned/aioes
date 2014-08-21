aioes reference
================

.. module:: aioes
   :synopsis: A library for accessing Elasticsearch server.
.. currentmodule:: aioes


Elasticsearch
-----------------


.. class:: Elasticsearch

   Class for operating on Elasticsearch cluster.

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

      :returns: resulting JSON

   .. seealso::

      `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_
