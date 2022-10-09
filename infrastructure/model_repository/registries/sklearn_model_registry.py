from dataclasses import dataclass

from sklearn.linear_model import (
    LinearRegression
)

from infrastructure.service import (
    ServiceConfig
)


@dataclass
class SKLearnModelRegistryConfig(ServiceConfig):
    """"""


class SKLearnModelRegistry:

    resource_config = SKLearnModelRegistryConfig

    model_classes = {
        LinearRegression.__name__: LinearRegression
    }

    def get(self, model_name: str, model_location: str, *args, **kwargs):
        model_class = self.model_classes[model_name]

        return model_class

    def put(self, *args, **kwargs):
        raise RuntimeError('Cannot `put` with {self.__class__.__name__}')
