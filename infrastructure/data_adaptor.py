from abc import ABC, abstractmethod
from typing import Any, Optional

from infrastructure.adaptor_clients.s3_client import S3Client
from infrastructure.service import Service, ServiceResult


class AdaptorResult(ServiceResult):
    ...


class AdaptorClient(ABC):
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
    """

    clients = {S3Client.__name__: S3Client}

    def __init__(self, client_name: str, override_init_config: Optional[dict] = None):
        client = self.clients[client_name]

        if override_init_config:
            client_config = client.resource_config.from_dict(override_init_config)
            self.client = client(client_config)
        else:
            self.client = client()

    def get(
        self, data_identifier: str, location: str, *args, **kwargs
    ) -> AdaptorResult:
        data = self.client.get(data_identifier, location, *args, **kwargs)

        return AdaptorResult(result=data)

    def put(
        self, data_identifier: str, location: str, value: Any, *args, **kwargs
    ) -> AdaptorResult:
        data = self.client.put(data_identifier, location, value, *args, **kwargs)

        return AdaptorResult(result=data)
