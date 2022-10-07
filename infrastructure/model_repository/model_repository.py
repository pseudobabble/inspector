from dataclasses import dataclass

from .service import Service, ServiceConfig
from .registries.hf_model_registry import HFModelRegistry
from .registries.s3_model_registry import S3ModelRegistry
from .registries.mlflow_model_registry import MLFlowModelRegistry



@dataclass
class ModelRepositoryConfig(ServiceConfig):
    """
    This class is designed to hold ModelPersister __init__ configuration.

    The class will be used like:

    ```
    persister_config = ModelPersisterConfig(
        some_kwarg=some_value,
        etc=etc
    )
    persister = MyModelPersister.configure(**persister_config)
    ```
    """


class ModelRepository(Service):
    """
    This class is designed to provide a common interface for all model persisters.

    You should subclass this class for your use case, and implement the `persist`
    and `retrieve` methods.
    """


    registries = {
        'hf_model_registry': HFModelRegistry,
        's3_model_registry': S3ModelRegistry,
        'mlflow_model_registry': MLFlowModelRegistry
    }

    def __init__(self, registry_name: str, override_init_config: Optional[dict] = None):
        registry = self.registries[registry_name]
        registry_config = registry.config.from_dict(override_init_config)

        if override_init_config:
            self.registry = registry(registry_config)
        else:
            self.registry = registry()

    def get(self, location, model_identifier, *args, **kwargs):
        return self.registry.get(location, model_identifier, args, kwargs)

    def put(self, location, model_identifier, model, *args, **kwargs):
        return self.registry.put(location, model_identifier, model, args, kwargs)
