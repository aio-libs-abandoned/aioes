asyncio client library for elasticsearch
=========================================

**aioes** is a asyncio_ compatible library for working with ElasticSearch_

Documentation
-------------

Read **aioes** documentation on Read The Docs: http://aioes.readthedocs.org/

Example
-------

::

    import asyncio
    from aioes import Elasticsearch

    @asyncio.coroutine
    def go():
        es = Elasticsearch(['localhost:9200'])
        ret = yield from es.create(index="my-index",
                                   doc_type="test-type",
                                   id=42,
                                   body={"str": "data",
                                         "int": 1})
        assert (ret == {'_id': '42',
                        '_index': 'my-index',
                        '_type': 'test-type',
                        '_version': 1,
                        'ok': True})

        answer = yield from es.get(index="my-index",
                                   doc_type="test-type",
                                   id=42)
        assert answer['_source'] == {'str': 'data', 'int': 1}

    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())


Requirements
------------

* Python_ 3.3+
* asyncio_ or Python 3.4+
* aiohttp_ 0.9.1+


Tests
-----

Make sure you have an instance of elastic-search running on port 9200
before executing the tests.

In order for all tests to work you need to add the following lines in the
`config/elasticsearch.yml` configuration file:

Enable groovy scripts::

  script.groovy.sandbox.enabled: true

Set a repository path::

  path.repo: ["/tmp"]


The test suite uses `nose`, to execute::

  nosetests tests


License
-------

aioes is offered under the BSD license.

.. _python: https://www.python.org/downloads/
.. _asyncio: https://pypi.python.org/pypi/asyncio
.. _aiohttp: https://pypi.python.org/pypi/aiohttp
.. _ElasticSearch: http://www.elasticsearch.org/
