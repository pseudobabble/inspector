import io

import numpy as np
import onnx
from dagster import In, Out, op
from onnxruntime import InferenceSession


@op(
    config_schema={"data_identifier": str, "location": str},
    required_resource_keys={
        #        "mlflow",
        "data_adaptor",
        "data_processor",
    },
)
def get_data(context):
    config = context.op_config
    logger = context.log
    #    mlflow = context.resources.mlflow
    data_adaptor = context.resources.data_adaptor
    data_processor = context.resources.data_processor

    data_identifier = config["data_identifier"]
    location = config["location"]
    #    mlflow.log_params({'data_identifier': data_identifier})
    logger.info("Getting dataset: %s", data_identifier)
    data = data_adaptor.get(data_identifier, location)
    logger.info(data)
    dataset = data_processor.process(data)

    return dataset


@op(
    config_schema={"model_identifier": str, "model_location": str},
    required_resource_keys={"get_model_repository"},
)
def load_model(context):
    logger = context.log
    config = context.op_config

    model_repository = context.resources.get_model_repository

    model_identifier = config["model_identifier"]
    model_location = config["model_location"]
    logger.info("Getting model %s from location %s", model_identifier, model_location)
    model = model_repository.get(model_identifier, model_location)

    return model


@op(ins={"model": In(), "data": In()})
def onnx_predict(context, model, data):
    logger = context.log
    config = context.op_config
    logger.info("started onnx_predict")

    # Convert BytesIO object to raw bytes
    # move this to the s3modelregistry
    if isinstance(model, bytes):
        model = model
        logger.info("model is bytes")
    elif isinstance(model, io.BytesIO):
        model = model.getvalue()
        logger.info("model converted to bytes")
    else:
        raise RuntimeError(f"Model should be bytes or BytesIO, got {type(model)}")

    try:
        onnx_model = onnx.load(io.BytesIO(model))  # Or from bytes
        logger.info(f"Model opset version: {onnx_model.opset_import[0].version}")
        logger.info(f"Model IR version: {onnx_model.ir_version}")
    except Exception as e:
        raise RuntimeError(f"Invalid model: {e}")

    try:
        onnx_model = onnx.load(io.BytesIO(model))
        onnx.checker.check_model(onnx_model)
        logger.info("Model validated")
    except Exception as e:
        raise RuntimeError(f"Invalid model: {e}")

    onnx_inference_session = InferenceSession(
        model,
        providers=[
            "TensorrtExecutionProvider",
            "CUDAExecutionProvider",
            "CPUExecutionProvider",
        ],
    )
    input_name = onnx_inference_session.get_inputs()[0].name
    label_name = onnx_inference_session.get_outputs()[0].name

    logger.info(f"input name: {input_name}")
    logger.info(f"label name: {label_name}")
    predictions = onnx_inference_session.run(
        [label_name], {input_name: data.evaluate.X}
    )
    logger.info(f"Predictions: {predictions}")

    return predictions
