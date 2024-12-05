import io
from dataclasses import asdict, dataclass
from typing import Any

from minio import Minio

from infrastructure.service import ServiceConfig

# from skl2onnx import convert_sklearn, to_onnx



@dataclass
class SKLearnConverterConfig(ServiceConfig):
    """"""


class SKLearnConverter:
    resource_config = SKLearnConverterConfig

    def __init__(self, config: SKLearnConverterConfig = None):
        config = config

    def convert(self, model, input_types, *args, **kwargs):
        # onnx_model = to_onnx(
        #     model, X=input_types
        # )

        # return onnx_model.SerializeToString()
        return
