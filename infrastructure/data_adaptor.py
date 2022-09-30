from abc import ABC, abstractmethod

from .service import Service

class DataAdapterConfig(dict):
    """
    This class is designed to hold DataAdapter __init__ configuration.

    The class will be used like:

    ```
    persister_config = DataAdapterConfig(
        some_kwarg=some_value,
        etc=etc
    )
    persister = MyDataAdapter(**persister_config)
    ```
    """


class DataAdapter(ABC, Service):
    """
    This class is designed to provide a common interface for all model persisters.

    You should subclass this class for your use case, and implement the `get` and
    `put` methods.
    """

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError('You must implement `get` for {self._class_._name_}')

    @abstractmethod
    def put(self, *args, **kwargs):
        raise NotImplementedError('You must implement `put` for {self._class_._name_}')
