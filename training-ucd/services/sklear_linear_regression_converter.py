import io
from dataclasses import asdict, dataclass
from typing import Any

from minio import Minio
from skl2onnx import convert_sklearn, to_onnx

from infrastructure.service import ServiceConfig


@dataclass
class SKLearnLinearRegressionConverterConfig(ServiceConfig):
    """"""


class SKLearnLinearRegressionConverter:
    resource_config = SKLearnLinearRegressionConverterConfig

    def __init__(self, config: SKLearnLinearRegressionConverterConfig = None):
        config = config

    def convert(self, model, input_types, *args, **kwargs):
        onnx_model = to_onnx(model, X=input_types)

        return onnx_model.SerializeToString()
