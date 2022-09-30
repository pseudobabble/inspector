from abc import ABC, abstractmethod

from .service import Service

class ModelRepositoryConfig(dict):
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


class ModelRepository(ABC, Service):
    """
    This class is designed to provide a common interface for all model persisters.

    You should subclass this class for your use case, and implement the `persist`
    and `retrieve` methods.
    """

    @abstractmethod
    def persist(self, *args, **kwargs):
        raise NotImplementedError('You must implement `persist` for {self._class_._name_}')


    @abstractmethod
    def retrieve(self, *args, **kwargs):
        raise NotImplementedError('You must implement `retrieve` for {self._class_._name_}')
