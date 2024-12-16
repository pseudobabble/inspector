import io
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
from minio import Minio
from skl2onnx import convert_sklearn, to_onnx

from infrastructure.service import ServiceConfig


@dataclass
class SKLearnLinearRegressionConverterConfig(ServiceConfig):
    """"""

    opset = int


class SKLearnLinearRegressionConverter:
    resource_config = SKLearnLinearRegressionConverterConfig

    def __init__(self, config: SKLearnLinearRegressionConverterConfig = None):
        config = config

    def convert(self, model, input_types, logger, *args, **kwargs):
        # Validate input data
        # if not isinstance(input_types, np.ndarray):
        #     raise ValueError("input_types must be a NumPy array")

        # logger.info(f"Converting model with input shape: {input_types.shape}")

        try:
            # Convert to ONNX format
            onnx_model = to_onnx(model, X=input_types, target_opset=11)
            logger.info("Model successfully converted to ONNX format")

            # Serialize to string
            serialized_model = onnx_model.SerializeToString()
            logger.info("Model successfully serialized to bytes")

            return serialized_model
        except Exception as e:
            logger.info(f"Error during ONNX conversion: {e}")
            raise e
