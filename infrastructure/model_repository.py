from abc import ABC
from typing import Optional

from infrastructure.registries.s3_model_registry import S3ModelRegistry
from infrastructure.service import Service, ServiceResult


class RepositoryResult(ServiceResult):
    ...


class Repository(ABC)
    def get(self, *args, **kwargs) -> ConverterResult:
        raise NotImplementedError(
            f"You must implement `get` on {self.__class__.__name__}"
        )

    def put(self, *args, **kwargs) -> ConverterResult:
        raise NotImplementedError(
            f"You must implement `put` on {self.__class__.__name__}"
        )


class ModelRepository(Service):
    """
    This class is designed to provide a common interface for all model persisters.

    You should subclass this class for your use case, and implement the `persist`
    and `retrieve` methods.
    """


    registries = {
        S3ModelRegistry.__name__: S3ModelRegistry,
    }

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
