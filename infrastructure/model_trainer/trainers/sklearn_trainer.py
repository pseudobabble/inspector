from dataclasses import dataclass

from infrastructure.service import ServiceConfig


class SKLearnTrainerConfig(ServiceConfig):
    """"""


class SKLearnTrainer:
    """
    This class is designed to provide a common interface for all data trainers.

    You should subclass this class for your use case, and implement the `train`
    method.
    """

    resource_config = SKLearnTrainerConfig

    def train(self, model, dataset, *args, **kwargs):
        trained_model = model.fit(dataset.train.X, dataset.train.y, *args)

        return trained_model
