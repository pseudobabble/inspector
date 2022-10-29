from dagster import graph

from ops.training import get_data

from ops.predict import (
    load_model,
    onnx_predict
)


@graph
def predict():
    model = load_model()
    data = get_data()
    predictions = onnx_predict(model, data)
    # do something with predictions
