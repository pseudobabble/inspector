from dagster import graph
from ops.training import (convert_model, get_data, get_model, save_model,
                          train_model)


@graph
def train():
    model = get_model()
    data = get_data()
    trained_model = train_model(model, data)
    converted_model = convert_model(trained_model)
    save_model(converted_model)
