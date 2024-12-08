from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from infrastructure.service import Service, ServiceConfig, ServiceResult


class TrainerResult(ServiceResult):
    """
    This class represents the result of model training.

    All Trainer.train calls should return an instance of this class
    """


@dataclass
class TrainerConfig(ServiceConfig):
    """
    This class is designed to hold Trainer __init__ configuration.

    The class will be used like:

    ```
    trainer_config = TrainerConfig(
        some_kwarg=some_value,
        etc=etc
    )
    trainer = MyTrainer(trainer_config)
    ```
    """


class Trainer(ABC):
    """
    This class is designed to provide a common interface for all data trainers.

    You should subclass this class for your use case, and implement the `train`
    method.
    """

    resource_config: Optional[TrainerConfig]

    @abstractmethod
    def train(
        self, model: ServiceResult, data: ServiceResult, *args, **kwargs
    ) -> TrainerResult:
        raise NotImplementedError(
            "You must implement `train` on {self.__class__.__name__}`"
        )


class ModelTrainer(Service):
    trainers = {}

    def __init__(self, trainer_name: str, override_init_config: Optional[dict] = None):
        trainer = self.trainers[trainer_name]

        if override_init_config:
            trainer_config = trainer.resource_config.from_dict(override_init_config)
            self.trainer = trainer(trainer_config)
        else:
            self.trainer = trainer()

    def train(self, model: ServiceResult, data: ServiceResult, *args, **kwargs):
        trained_model = self.trainer.train(model, data, *args, **kwargs)

        return trained_model
