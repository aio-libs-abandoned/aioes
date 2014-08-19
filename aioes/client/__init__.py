import weakref

from .indices import IndicesClient


class Elasticsearch:
    def __init__(self):
        self._indices = weakref.ref(IndicesClient(self))
        # self._cluster = weakref.ref(ClusterClient(self))
        # self._cat = weakref.ref(CatClient(self))
        # self._nodes = weakref.ref(NodesClient(self))
        # self._snapshot = weakref.ref(SnapshotClient(self))

    @property
    def indices(self):
        return self._indices()

    @property
    def cluster(self):
        return self._cluster()

    @property
    def cat(self):
        return self._cat()

    @property
    def nodes(self):
        return self._nodes()

    @property
    def snapshot(self):
        return self._snapshot()

    def __repr__(self):
        pass

    def ping(self):
        pass

    def info(self):
        pass

    def create(self):
        pass

    def index(self):
        pass

    def exists(self):
        pass

    def get(self):
        pass

    def get_source(self):
        pass

    def mget(self):
        pass

    def update(self):
        pass

    def search(self):
        pass

    def search_shards(self):
        pass

    def search_template(self):
        pass

    def explain(self):
        pass

    def scroll(self):
        pass

    def clear_scroll(self):
        pass

    def delete(self):
        pass

    def count(self):
        pass

    def bulk(self):
        pass

    def msearch(self):
        pass

    def delete_by_query(self):
        pass

    def suggest(self):
        pass

    def percolate(self):
        pass

    def mpercolate(self):
        pass

    def count_percolate(self):
        pass

    def mlt(self):
        pass

    def termvector(self):
        pass

    def mtermvectors(self):
        pass

    def benchmark(self):
        pass

    def abort_benchmark(self):
        pass

    def list_enchmark(self):
        pass

    def put_script(self):
        pass

    def get_script(self):
        pass

    def delete_script(self):
        pass

    def put_template(self):
        pass

    def get_template(self):
        pass

    def delete_template(self):
        pass
