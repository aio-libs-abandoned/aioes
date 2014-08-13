class NamespacedClient:

    def __init__(self, client):
        self._client = client

    @property
    def client(self):
        return self._client

    @property
    def transport(self):
        return self._client.transport
