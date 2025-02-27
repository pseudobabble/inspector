from dataclasses import dataclass

from sklearn.pipeline import Pipeline
from skl2onnx.algebra.type_helper import guess_initial_types

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
        trained_model = model().fit(X=dataset.train.X, y=dataset.train.y, *args)
        input_types = guess_initial_types(dataset.train.X, None)
        return trained_model, input_types
