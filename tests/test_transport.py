import asyncio
import time
import unittest
import urllib.parse

from aioes.transport import Endpoint, Transport


class TestTransport(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def make_transport(self, endpoints=[{'host': 'localhost'}],
                       sniffer_interval=None):
        tr = Transport(endpoints, loop=self.loop,
                       sniffer_interval=sniffer_interval)
        self.addCleanup(tr.close)
        return tr

    def test_ctor(self):
        tr = self.make_transport()
        self.assertEqual(3, tr.max_retries)
        self.assertGreaterEqual(time.monotonic(), tr.last_sniff)
        self.assertIsNone(tr.sniffer_interval)
        self.assertAlmostEqual(0.1, tr.sniffer_timeout)
        self.assertEqual([Endpoint('http', 'localhost', 9200)], tr.endpoints)
        self.assertEqual(1, len(tr._pool.connections))

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

    def test_set_endpoints(self):
        tr = self.make_transport([])
        self.assertEqual([], tr.endpoints)
        tr.endpoints = [{'host': 'localhost'}]
        self.assertEqual([Endpoint('http', 'localhost', 9200)], tr.endpoints)
        self.assertEqual(1, len(tr._pool.connections))

    def test_set_endpoints_Endpoint(self):
        tr = self.make_transport([])
        self.assertEqual([], tr.endpoints)
        tr.endpoints = [Endpoint('http', 'localhost', 9200)]
        self.assertEqual([Endpoint('http', 'localhost', 9200)], tr.endpoints)
        self.assertEqual(1, len(tr._pool.connections))

    def test_dont_recreate_existing_connections(self):
        tr = self.make_transport()
        connections = tr._pool.connections
        tr.endpoints = [{'host': 'localhost'}]
        self.assertEqual([Endpoint('http', 'localhost', 9200)], tr.endpoints)
        self.assertEqual(connections, tr._pool.connections)

    def test_set_malformed_endpoints(self):
        tr = self.make_transport()
        with self.assertRaises(RuntimeError):
            tr.endpoints = [123]
        self.assertEqual([Endpoint('http', 'localhost', 9200)], tr.endpoints)
        self.assertEqual(1, len(tr._pool.connections))

    def test_set_host_only_string(self):
        tr = self.make_transport()
        tr.endpoints = ['host']
        self.assertEqual([Endpoint('http', 'host', 9200)], tr.endpoints)
        self.assertEqual(1, len(tr._pool.connections))

    def test_set_host_port_string(self):
        tr = self.make_transport()
        tr.endpoints = ['host:123']
        self.assertEqual([Endpoint('http', 'host', 123)], tr.endpoints)
        self.assertEqual(1, len(tr._pool.connections))

    def test_set_host_port_string_invalid(self):
        tr = self.make_transport()
        with self.assertRaises(RuntimeError):
            tr.endpoints = ['host:123:abc']
        self.assertEqual([Endpoint('http', 'localhost', 9200)], tr.endpoints)
        self.assertEqual(1, len(tr._pool.connections))

    def test_set_host_dict_invalid(self):
        tr = self.make_transport()
        with self.assertRaises(RuntimeError):
            tr.endpoints = [{'a': 'b'}]
        self.assertEqual([Endpoint('http', 'localhost', 9200)], tr.endpoints)
        self.assertEqual(1, len(tr._pool.connections))

    def test_username_password_endpoints_with_port(self):
        tr = self.make_transport(endpoints=['john:doe@localhost:9200'])
        self.assertEqual([Endpoint('http', 'john:doe@localhost', 9200)],
                         tr.endpoints)

    def test_username_password_endpoints_without_port(self):
        tr = self.make_transport(endpoints=['john:doe@localhost'])
        self.assertEqual([Endpoint('http', 'john:doe@localhost', 9200)],
                         tr.endpoints)

    def test_username_password_endpoints_with_port_https(self):
        tr = self.make_transport(endpoints=['https://john:doe@localhost:9200'])
        self.assertEqual([Endpoint('https', 'john:doe@localhost', 9200)],
                         tr.endpoints)
        self.assertEqual(
            ('https', 'john:doe@localhost:9200', '/', '', '', ''),
            tuple(urllib.parse.urlparse(tr._pool.connections[0]._base_url))
        )

    def test_bad_schema(self):
        with self.assertRaises(RuntimeError):
            self.make_transport(endpoints=['s3://john:doe@localhost:9200'])

    def test_default_port_https(self):
        tr = self.make_transport(endpoints=['https://localhost'])
        self.assertEqual([Endpoint('https', 'localhost', 443)],
                         tr.endpoints)

    def test_default_port_http(self):
        tr = self.make_transport(endpoints=['http://localhost'])
        self.assertEqual([Endpoint('http', 'localhost', 9200)],
                         tr.endpoints)

    def test_sniff(self):
        tr = self.make_transport(sniffer_interval=0.001)

        @asyncio.coroutine
        def go():
            t0 = time.monotonic()
            yield from asyncio.sleep(0.001, loop=self.loop)
            yield from tr.get_connection()
            self.assertGreater(tr.last_sniff, t0)

        self.loop.run_until_complete(go())

    def test_get_connection_without_sniffing(self):
        tr = self.make_transport(sniffer_interval=1000)

        @asyncio.coroutine
        def go():
            t0 = tr.last_sniff
            yield from tr.get_connection()
            self.assertEqual(t0, tr.last_sniff)

        self.loop.run_until_complete(go())

    @unittest.expectedFailure
    def test__mark_dead(self):
        tr = self.make_transport()

        @asyncio.coroutine
        def go():
            conn = yield from tr.get_connection()
            last_sniff = tr.last_sniff
            yield from tr._mark_dead(conn)
            self.assertGreater(tr.last_sniff, last_sniff)
            self.assertEqual(1, tr._pool._dead_count[conn])

        self.loop.run_until_complete(go())

    def test_perform_request_body_bytes(self):
        tr = self.make_transport()

        @asyncio.coroutine
        def go():
            status, data = yield from tr.perform_request(
                'GET', '/_nodes/_all', body=b'')

        self.loop.run_until_complete(go())
