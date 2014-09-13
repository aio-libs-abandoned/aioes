"""Compare tool.

Calculate difference between public API from `elasticsearch` and `aioes`.
"""

from elasticsearch import Elasticsearch as es
from elasticsearch.client.utils import NamespacedClient
from aioes import Elasticsearch as aioes

es_set = {i for i in dir(es([])) if not i.startswith('_')}
aioes_set = {i for i in dir(aioes([])) if not i.startswith('_')}

print('-'*70)
print('Missing: ', ' '.join(sorted(es_set - aioes_set)))
print('Extra: ', ' '.join(sorted(aioes_set - es_set)))


obj = es([])
obj2 = aioes([])

for sub in dir(obj):
    if sub.startswith('_'):
        continue
    val = getattr(obj, sub)
    if isinstance(val, NamespacedClient):
        left = {i for i in dir(val) if not i.startswith('_')}
        val2 = getattr(obj2, sub, None)
        if val2 is None:
            continue
        right = {i for i in dir(val2) if not i.startswith('_')}
        print(' '*10, sub)
        print(' '*10, 'Missing: ', ' '.join(sorted(left - right)))
        print(' '*10, 'Extra: ', ' '.join(sorted(right - left)))
