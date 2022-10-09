from dagster import graph

from ops.training import (
    get_model,
    get_data,
    train_model,
    save_model
)

@graph
def train():
    model = get_model()
    data = get_data()
    trained_model = train_model(model, data)
    save_model(trained_model)
