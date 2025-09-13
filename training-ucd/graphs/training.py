from dagster import graph
from ops.training import (convert_model, get_data, get_model, save_model,
                          start_experiment, train_model)


@graph
def train():
    start = start_experiment()
    model = get_model(start=start)
    data = get_data(start=start)
    trained_model, model_inputs = train_model(model, data)
    converted_model = convert_model(trained_model, model_inputs)
    save_model(converted_model)
