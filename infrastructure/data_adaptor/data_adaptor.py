from .service import Service, ServiceConfig
from .service_clients.s3_client import S3Client




class DataAdaptor(Service):
    """
    This class is designed to provide a common interface for all model persisters.

    You should subclass this class for your use case, and implement the `get` and
    `put` methods.
    """

    clients = {
        "s3": S3Client
    }

    op_config = {yeah}

    def __init__(self, client_name: str, override_init_config: Optional[dict] = None):
        client = self.clients[client_name]
        client_config = client.config.from_dict(override_init_config)

        if override_init_config:
            self.client = client(client_config)
        else:
            self.client = client()

    def get(self, data_identifier: str, location: str, *args, **kwargs):
        return self.client.get(data_identifier, location, *args, **kwargs)

    def put(self, data_identifier: str, location: str, value: Any, *args, **kwargs):
        return self.client.put(data_identifier, location, value, *args, **kwargs)
