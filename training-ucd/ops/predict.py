import numpy as np
from dagster import In, Out, op

# from onnxruntime import InferenceSession


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

    # onnx_inference_session = InferenceSession(
    #     model,
    #     providers=[
    #         "TensorrtExecutionProvider",
    #         "CUDAExecutionProvider",
    #         "CPUExecutionProvider",
    #     ],
    # )
    # input_name = onnx_inference_session.get_inputs()[0].name
    # label_name = onnx_inference_session.get_outputs()[0].name

    # predictions = onnx_inference_session.run(
    #     [label_name], {input_name: data.evaluate.X}
    # )
    # logger.info(f"Predictions: {predictions}")
    logger.info("reached predict")

    return predictions
