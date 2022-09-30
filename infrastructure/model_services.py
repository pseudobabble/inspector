from abc import ABC, abstractmethod

from .service import Service

class ModelPersisterConfig(dict):
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


class ModelRetrieverConfig(dict):
    """
    This class is designed to hold ModelRetriever __init__ configuration.

    The class will be used like:

    ```
    retriever_config = ModelRetrieverConfig(
        some_kwarg=some_value,
        etc=etc
    )
    retriever = MyModelRetriever.configure(**retriever_config)
    ```
    """


class ModelPersister(ABC, Service):
    """
    This class is designed to provide a common interface for all model persisters.

    You should subclass this class for your use case, and implement the `persist`
    method.
    """

    @abstractmethod
    def persist(self, *args, **kwargs):
        raise NotImplementedError('You must implement `persist` for {self._class_._name_}')


class ModelRetriever(ABC, Service):
    """
    This class is designed to provide a common interface for all model retrievers.

    You should subclass this class for your use case, and implement the `retrieve`
    method.
    """

    @abstractmethod
    def retrieve(self, *args, **kwargs):
        raise NotImplementedError('You must implement `retrieve` for {self._class_._name_}')
