.. aioes documentation master file, created by
   sphinx-quickstart on Thu Aug 21 14:52:22 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

aioes
=====

.. _GitHub: https://github.com/aio-libs/aioes
.. _asyncio: http://docs.python.org/3.4/library/asyncio.html

**aioes** is a libarary for working with an :term:`ElasticSearch` from
:term:`asyncio` framework.

Features
--------

- Easy interface to :term:`ElasticSearch` cluster.
- Modelled after :term:`elasticsearch-py`. Not fully compatible due
  ``yield from`` nature of :term:`asyncio` but looks very simular.

Basic Example
-------------

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

Installation
------------

**aioes** published on *PyPI* and can be installed via ``pip`` tool::

    pip3 install aioes

Dependencies
------------

- Python 3.3 and :mod:`asyncio` or Python 3.4+
- :term:`aiohttp` 9.1+

Authors and License
-------------------

The ``aioes`` package is written by Andrew Svetlov.  It's BSD
licensed and freely available.

Feel free to improve this package and send a pull request to GitHub_.

Contents:

.. toctree::
   :maxdepth: 2

   reference
   glossary

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
