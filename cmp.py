"""Compare tool.

Calculate difference between public API from `elasticsearch` and `aioes`.
"""

import elasticsearch
from elasticsearch.client.utils import NamespacedClient
import aioes

endpoint = 'localhost:9200'
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
