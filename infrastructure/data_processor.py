from abc import ABC, abstractmethod

from .service import Service


class DataProcessorConfig(dict):
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


class DataProcessor(ABC, Service):
    """
    This class is designed to provide a common interface for all data processors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    @abstractmethod
    def process(self):
        raise NotImplementedError('You must implement `process` for {self._class_._name_}')
