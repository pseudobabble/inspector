import io
from dataclasses import dataclass

from transformers import (
    AutoModel,
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification
)

from infrastructure.service import (
    ServiceConfig
)


@dataclass
class HFModelRegistryConfig(ServiceConfig):
    """"""


class HFModelRegistry:

    resource_config = HFModelRegistryConfig

    model_classes = {
        AutoModel.__name__: AutoModel,
        AutoModelForTokenClassification.__name__: AutoModelForTokenClassification,
        AutoModelForSequenceClassification.__name__: AutoModelForSequenceClassification,
    }

    def get(self, model_name: str, model_class_name: str, *args, **kwargs):
        model_class = self.model_classes.get(model_class_name, AutoModel)

        return model_class.from_pretrained(model_name)

    def put(self, *args, **kwargs):
        raise RuntimeError('Cannot `put` with {self.__class__.__name__}')
