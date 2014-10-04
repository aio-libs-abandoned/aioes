asyncio client library for elasticsearch
=========================================

**aioes** is a asyncio_ compatible library for working with ElasticSearch_

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



License
-------

aioes is offered under the BSD license.

.. _python: https://www.python.org/downloads/
.. _asyncio: https://pypi.python.org/pypi/asyncio
.. _aiohttp: https://pypi.python.org/pypi/aiohttp
.. _ElasticSearch: http://www.elasticsearch.org/
