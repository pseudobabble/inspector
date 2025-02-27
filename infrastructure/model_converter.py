from abc import ABC
from dataclasses import dataclass
from typing import Optional

from infrastructure.service import Service, ServiceConfig, ServiceResult


class ConverterResult(ServiceResult):
    """
    This class provices a common interface for all results of ModelConverter.process
    """


@dataclass
class ConverterConfig(ServiceConfig):
    """
    This class is designed to hold Converter __init__ configuration.

    The class will be used like:

    ```
    converter_config = ConverterConfig(
        some_kwarg=some_value,
        etc=etc
    )
    converter = MyConverter(trainer_config)
    ```
    """


class Converter(ABC):
    resource_config = Optional[ConverterConfig]

    def convert(self, model: ServiceResult, *args, **kwargs) -> ConverterResult:
        raise NotImplementedError(
            f"You must implement `convert` on {self.__class__.__name__}"
        )


class ModelConverter(Service):
    """
    This class is designed to provide a common interface for all data converters.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    converters = {}

    def __init__(
        self, converter_name: str, override_init_config: Optional[dict] = None
    ):
        converter = self.converters[converter_name]

        if override_init_config:
            converter_config = converter.resource_config.from_dict(override_init_config)
            self.converter = converter(converter_config)
        else:
            self.converter = converter()

    def convert(self, model: ServiceResult, *args, **kwargs):
        converted_model = self.converter.convert(model, *args, **kwargs)

        return converted_model
