from abc import ABC
from dataclasses import dataclass
from typing import Optional

from infrastructure.service import Service, ServiceConfig, ServiceResult


class RepositoryResult(ServiceResult):
    ...


@dataclass
class RepositoryConfig(ServiceConfig):
    """
    This class is designed to hold Repository __init__ configuration.

    The class will be used like:

    ```
    repository_config = RepositoryConfig(
        some_kwarg=some_value,
        etc=etc
    )
    repository = MyRepository(trainer_config)
    ```
    """


class Repository(ABC):
    resource_config = Optional[RepositoryConfig]

    def get(self, *args, **kwargs):
        raise NotImplementedError(
            f"You must implement `get` on {self.__class__.__name__}"
        )

    def put(self, *args, **kwargs):
        raise NotImplementedError(
            f"You must implement `put` on {self.__class__.__name__}"
        )


class ModelRepository(Service):
    """
    This class is designed to provide a common interface for all model persisters.

    You should subclass this class for your use case, and implement the `persist`
    and `retrieve` methods.
    """

    registries = {}

    def __init__(self, registry_name: str, override_init_config: Optional[dict] = None):
        registry = self.registries[registry_name]

        if override_init_config:
            registry_config = registry.resource_config.from_dict(override_init_config)
            self.registry = registry(registry_config)
        else:
            self.registry = registry()

    def get(self, model_identifier: str, location: str, *args, **kwargs):
        model = self.registry.get(model_identifier, location, *args, **kwargs)

        return RepositoryResult(result=model)

    def put(self, model_identifier: str, location, model: str, *args, **kwargs):
        response = self.registry.put(model_identifier, location, model, *args, **kwargs)

        return RepositoryResult(result=response)
