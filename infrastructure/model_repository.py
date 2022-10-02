from abc import ABC, abstractmethod
from dataclasses import dataclass

from .service import Service, ServiceConfig


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

    def __init__(self, config: ModelRepositoryConfig):
        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, value)

    @abstractmethod
    def put(self, *args, **kwargs):
        raise NotImplementedError('You must implement `put` for {self._class_._name_}')


    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError('You must implement `get` for {self._class_._name_}')
