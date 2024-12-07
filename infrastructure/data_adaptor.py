from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from infrastructure.service import Service, ServiceConfig, ServiceResult


class AdaptorResult(ServiceResult):
    ...


@dataclass
class AdaptorConfig(ServiceConfig):
    """
    This class is designed to hold Adaptor __init__ configuration.

    The class will be used like:

    ```
    adaptor_config = AdaptorConfig(
        some_kwarg=some_value,
        etc=etc
    )
    adaptor = MyAdaptor(adaptor_config)
    ```
    """


class AdaptorClient(ABC):
    """ """

    resource_config = Optional[AdaptorConfig]

    @abstractmethod
    def get(self, *args, **kwargs) -> AdaptorResult:
        raise NotImplementedError(
            "You must implement `get` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def put(self, *args, **kwargs) -> AdaptorResult:
        raise NotImplementedError(
            "You must implement `put` on {self.__class__.__name__}`"
        )


class DataAdaptor(Service):
    """
    This class is designed to provide a common interface for all model persisters.

    You should subclass this class for your use case, and implement the `get` and
    `put` methods.

    Clients should be added to the service at the resource layer, as follows:
    ```
    DataAdaptor.clients.update({StorageClient.__name__: StorageClient})
    ```
    """

    clients = {}

    def __init__(self, client_name: str, override_init_config: Optional[dict] = None):
        client = self.clients[client_name]

        if override_init_config:
            client_config = client.resource_config.from_dict(override_init_config)
            self.client = client(client_config)
        else:
            self.client = client()

    def get(self, data_identifier: str, location: str, *args, **kwargs):
        data = self.client.get(data_identifier, location, *args, **kwargs)

        return data

    def put(self, data_identifier: str, location: str, value: Any, *args, **kwargs):
        data = self.client.put(data_identifier, location, value, *args, **kwargs)

        return data
