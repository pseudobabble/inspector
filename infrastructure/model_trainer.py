from abc import ABC, abstractmethod
from dataclasses import dataclass

from .service import Service, ServiceConfig


@dataclass
class ModelTrainerConfig(ServiceConfig):
    """
    This class is designed to hold Trainer __init__ configuration.

    The class will be used like:

    ```
    trainer_config = TrainerConfig(
        some_kwarg=some_value,
        etc=etc
    )
    trainer = MyTrainer.configure(trainer_config)
    ```
    """


class ModelTrainer(Service):
    """
    This class is designed to provide a common interface for all data trainers.

    You should subclass this class for your use case, and implement the `train`
    method.
    """

    @abstractmethod
    def train(self, *args, **kwargs):
        raise NotImplementedError('You must implement `train` for {self._class_._name_}')
