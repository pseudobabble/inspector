from dagster import graph

from ops.training import (
    get_pretrained_model,
    get_data,
    train_pretrained_model,
    save_model
)

@graph
def train_pretrained():
    model = get_pretrained_model()
    data = get_data()
    trained_model = train_pretrained_model(model, data)
    save_model(tuned_model)
