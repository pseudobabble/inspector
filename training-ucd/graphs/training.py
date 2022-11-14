from dagster import graph

from ops.training import (
    get_model,
    get_data,
    train_model,
    convert_model,
    save_model
)

@graph
def train():
    model = get_model()
    data = get_data()
    trained_model, model_inputs = train_model(model, data)
    converted_model = convert_model(trained_model, model_inputs)
    save_model(converted_model)
