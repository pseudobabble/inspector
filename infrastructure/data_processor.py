from abc import ABC, abstractmethod
from dataclasses import dataclass

from .service import Service, ServiceConfig


@dataclass
class DataProcessorConfig(ServiceConfig):
    """
    This class is designed to hold DataProcessor __init__ configuration.

    The class will be used like:

    ```
    processor_config = DataProcessorConfig(
        some_kwarg=some_value,
        etc=etc
    )
    processor = MyDataProcessor.configure(**processor_config)
    ```
    """


class DataProcessor(Service):
    """
    This class is designed to provide a common interface for all data processors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    @abstractmethod
    def process(self, *args, **kwargs):
        raise NotImplementedError('You must implement `process` for {self._class_._name_}')
