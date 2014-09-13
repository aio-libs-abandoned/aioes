"""Compare tool.

Calculate difference between public API from `elasticsearch` and `aioes`.
"""



from elasticsearch import Elasticsearch as es
from aioes import Elasticsearch as aioes

es_set = {i for i in dir(es([])) if not i.startswith('_')}
aioes_set = {i for i in dir(aioes([])) if not i.startswith('_')}

print('Missing: ', sorted(es_set - aioes_set))
print('Extra: ', sorted(aioes_set - es_set))
