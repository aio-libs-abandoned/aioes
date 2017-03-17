"""Compare tool.

Calculate difference between public API from `elasticsearch` and `aioes`.
"""

import elasticsearch
import docker
import os
import socket
import time
import contextlib
from elasticsearch.client.utils import NamespacedClient
import aioes


@contextlib.contextmanager
def find_endpoint():
    if os.environ.get("NO_DOCKER"):
        yield ('localhost', 9200)
    else:
        es_tag = os.environ.get("ES_VERSION", '2.4')
        cl = docker.Client(version='auto')
        cl.pull('elasticsearch:{}'.format(es_tag))
        container = cl.create_container(
            image='elasticsearch:{}'.format(es_tag),
            name='aioes-test-server',
            ports=[9200],
            detach=True)
        cid = container['Id']
        cl.start(container=cid)
        ins = cl.inspect_container(cid)
        try:
            yield (ins['NetworkSettings']['IPAddress'], 9200)
        finally:
            cl.kill(container=cid)
            cl.remove_container(cid)


def wait_connect(endpoint):
    delay = .001
    for _ in range(100):
        try:
            with socket.socket() as sock:
                sock.connect(endpoint)
                break
        except OSError:
            time.sleep(delay)
            delay *= 2


def main(endpoint):
    es_client = elasticsearch.Elasticsearch([endpoint])
    aioes_client = aioes.Elasticsearch([endpoint])

    version = es_client.info()['version']
    print('-'*70)
    print('ElasticSearch (server): {}'.format(version['number']))
    print('elasticsearch-py: {}'.format(elasticsearch.__version__))

    es_set = {i for i in dir(es_client) if not i.startswith('_')}
    aioes_set = {i for i in dir(aioes_client) if not i.startswith('_')}

    print('-'*70)
    print('Missing: ', ' '.join(sorted(es_set - aioes_set)))
    print('Extra: ', ' '.join(sorted(aioes_set - es_set)))

    for sub in dir(es_client):
        if sub.startswith('_'):
            continue
        val = getattr(es_client, sub)
        if isinstance(val, NamespacedClient):
            left = {i for i in dir(val) if not i.startswith('_')}
            val2 = getattr(aioes_client, sub, None)
            if val2 is None:
                continue
            right = {i for i in dir(val2) if not i.startswith('_')}
            print(' '*6, sub)
            print(' '*10, 'Missing: ', ' '.join(sorted(left - right)))
            print(' '*10, 'Extra: ', ' '.join(sorted(right - left)))


if __name__ == '__main__':
    with find_endpoint() as endpoint:
        wait_connect(endpoint)
        main('{}:{}'.format(*endpoint))
