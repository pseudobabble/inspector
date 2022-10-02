import io
from dataclasses import dataclass

from transformers import (
    AutoModel,
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification
)

from infrastructure.model_repository import (
    ModelRepositoryConfig,
    ModelRepository
)


@dataclass
class HFModelRepositoryConfig(ModelRepositoryConfig):
    """"""

class HFModelRepository(ModelRepositoryConfig):

    model_classes = {
        AutoModelForTokenClassification.__name__: AutoModelForTokenClassification,
        AutoModelForSequenceClassification.__name__: AutoModelForSequenceClassification,
    }

    def __init__(self, config: ModelRepositoryConfig):
        super().__init__(config)

    def get(self, model_name: str, model_class_name: str):
        model_class = self.model_classes.get(model_class_name, AutoModel)

        return model_class.from_pretrained(model_name)

    def put(self, *args, **kwargs):
        raise RuntimeError('Cannot `put` with {self.__class__.__name__}')
