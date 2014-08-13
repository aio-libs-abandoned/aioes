from .utils import NamespacedClient


class IndicesClient(NamespacedClient):

    def analyze(self):
        pass

    def refresh(self):
        pass

    def flush(self):
        pass

    def create(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

    def delete(self):
        pass

    def exists(self):
        pass

    def exists_type(self):
        pass

    def put_mapping(self):
        pass

    def get_mapping(self):
        pass

    def get_field_mapping(self):
        pass

    def delete_mapping(self):
        pass

    def put_alias(self):
        pass

    def exists_alias(self):
        pass

    def get_alias(self):
        pass

    def get_aliases(self):
        pass

    def update_aliases(self):
        pass

    def delete_alias(self):
        pass

    def put_template(self):
        pass

    def exists_template(self):
        pass

    def get_template(self):
        pass

    def delete_template(self):
        pass

    def get_settings(self):
        pass

    def put_settings(self):
        pass

    def put_warmer(self):
        pass

    def get_warmer(self):
        pass

    def delete_warmer(self):
        pass

    def status(self):
        pass

    def stats(self):
        pass

    def segments(self):
        pass

    def optimize(self):
        pass

    def validate_query(self):
        pass

    def clear_cache(self):
        pass

    def recovery(self):
        pass

    def snapshot_index(self):
        pass
