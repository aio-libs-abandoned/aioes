import asyncio
import time
import unittest


from aioes.transport import Endpoint, Transport


class TestTransport(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def make_transport(self):
        tr = Transport([{'host': 'localhost'}], loop=self.loop)
        self.addCleanup(tr.close)
        return tr

    def test_ctor(self):
        tr = self.make_transport()
        self.assertEqual(3, tr.max_retries)
        self.assertGreaterEqual(time.monotonic(), tr.last_sniff)
        self.assertEqual([Endpoint('localhost', 9200)], tr.endpoints)

    def test_simple(self):
        tr = self.make_transport()
        @asyncio.coroutine
        def go():
            body, headers, node_info = yield from tr.perform_request(
                'GET', '/_nodes/_all/clear')
            print(body)
            print(headers)
            print(node_info)
        self.loop.run_until_complete(go())
