from typing import Optional
from dataclasses import dataclass

from infrastructure.service import Service, ServiceConfig

# from something import ONNXModelConverter


class ModelConverter(Service):
    """
    This class is designed to provide a common interface for all data converters.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    converters = {
    }

    def __init__(self, converter_name: str, override_init_config: Optional[dict] = None):
        converter = self.converters[converter_name]

        if override_init_config:
            converter_config = converter.resource_config.from_dict(
                override_init_config)
            self.converter = converter(converter_config)
        else:
            self.converter = converter()

    def convert(self, model, input_types, *args, **kwargs):
        return self.converter.convert(model, input_types, *args, **kwargs)
