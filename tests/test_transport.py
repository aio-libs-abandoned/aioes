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
        self.assertIsNone(tr.sniffer_interval)
        self.assertAlmostEqual(0.1, tr.sniffer_timeout)
        self.assertEqual([Endpoint('localhost', 9200)], tr.endpoints)

    def test_simple(self):
        tr = self.make_transport()

        @asyncio.coroutine
        def go():
            status, data = yield from tr.perform_request(
                'GET', '/_nodes/_all/clear')
            self.assertEqual(200, status)
            self.assertIn('nodes', data)
            # self.assertEqual(
            #     {'nodes':
            #      {'kagIbHGHS3a0dcyPmp0Jkw':
            #       {'version': '1.3.1',
            #        'ip': '127.0.1.1',
            #        'build': '2de6dc5',
            #        'name': 'Mandrill',
            #        'transport_address':
            #        'inet[/192.168.0.183:9300]',
            #        'http_address': 'inet[/192.168.0.183:9200]',
            #        'host': 'andrew-levelup'}},
            #      'cluster_name': 'elasticsearch'}, data)
        self.loop.run_until_complete(go())
