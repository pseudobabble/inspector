from dataclasses import dataclass

from diffusers import StableDiffusionPipeline
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
    from_pretrained: dict


class HFModelRegistry:

    resource_config = HFModelRegistryConfig

    def __init__(self, config: HFModelRegistryConfig = None):
        self.config = config

    model_classes = {
        AutoModel.__name__: AutoModel,
        AutoModelForTokenClassification.__name__: AutoModelForTokenClassification,
        AutoModelForSequenceClassification.__name__: AutoModelForSequenceClassification,
        StableDiffusionPipeline.__name__: StableDiffusionPipeline
    }

    def get(self, model_name: str, model_class_name: str, *args, **kwargs):
        model_class = self.model_classes.get(model_class_name, AutoModel)

        from_pretrained_args = self.config.get('from_pretrained', {})
        return model_class.from_pretrained(model_name, **from_pretrained_args)

    def put(self, *args, **kwargs):
        raise RuntimeError('Cannot `put` with {self.__class__.__name__}')
