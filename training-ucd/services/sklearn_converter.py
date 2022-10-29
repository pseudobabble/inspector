import io
from typing import Any
from dataclasses import dataclass, asdict

from minio import Minio
from skl2onnx import convert_sklearn
from skl2onnx import to_onnx

from infrastructure.service import ServiceConfig


@dataclass
class SKLearnConverterConfig(ServiceConfig):
    """"""


class SKLearnConverter:

    resource_config = SKLearnConverterConfig

    def __init__(self, config: SKLearnConverterConfig = None):
        config = config

    def convert(self, model, input_types, *args, **kwargs):
        onnx_model = to_onnx(
            model, X=input_types
        )

        return onnx_model.SerializeToString()
