from typing import Optional

from infrastructure.service import Service

from .registries.hf_model_registry import HFModelRegistry
from .registries.s3_model_registry import S3ModelRegistry



class ModelRepository(Service):
    """
    This class is designed to provide a common interface for all model persisters.

    You should subclass this class for your use case, and implement the `persist`
    and `retrieve` methods.
    """


    registries = {
        'hf_model_registry': HFModelRegistry,
        's3_model_registry': S3ModelRegistry
    }

    def __init__(self, registry_name: str, override_init_config: Optional[dict] = None):
        registry = self.registries[registry_name]

        if override_init_config:
            registry_config = registry.resource_config.from_dict(override_init_config)
            self.registry = registry(registry_config)
        else:
            self.registry = registry()

    def get(self, model_identifier: str, location: str, *args, **kwargs):
        return self.registry.get(model_identifier, location, *args, **kwargs)

    def put(self, model_identifier: str, location, model: str, *args, **kwargs):
        return self.registry.put(model_identifier, location, model, *args, **kwargs)
