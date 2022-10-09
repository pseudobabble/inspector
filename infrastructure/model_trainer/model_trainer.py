from abc import ABC, abstractmethod
from dataclasses import dataclass

from .service import ServiceConfig

from .trainers.sklearn_trainer import SKLearnTrainer



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


class ModelTrainer:
    """
    This class is designed to provide a common interface for all data trainers.

    You should subclass this class for your use case, and implement the `train`
    method.
    """

    trainers = {
        SKLearnTrainer.__name__: SKLearnTrainer
    }

    def __init__(self, trainer_name: str, override_init_config: Optional[dict] = None):
        trainer = self.trainers[trainer_name]

        if override_init_config:
            trainer_config = trainer.resource_config.from_dict(override_init_config)
            self.trainer = trainer(trainer_config)
        else:
            self.trainer = trainer()

    def train(self, model, data, *args, **kwargs):
        return self.trainer.train(model, data, *args, **kwargs)
