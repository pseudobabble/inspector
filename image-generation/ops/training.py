from dagster import In, Out, op


@op(
    config_schema={"model_identifier": str, "model_location": str},
    required_resource_keys={"get_model_model_repository"},
)
def get_model(context):
    logger = context.log
    config = context.op_config

    model_repository = context.resources.get_model_model_repository

    model_identifier = config["model_identifier"]
    model_location = config["model_location"]
    logger.info("Getting model %s from location %s", model_identifier, model_location)
    model = model_repository.get(model_identifier, model_location)

    return model


@op(
    config_schema={"data_identifier": str, "location": str},
    required_resource_keys={"mlflow", "data_adaptor", "data_processor"},
)
def get_data(context):
    config = context.op_config
    logger = context.log
    mlflow = context.resources.mlflow
    data_adaptor = context.resources.data_adaptor
    data_processor = context.resources.data_processor

    data_identifier = config["data_identifier"]
    location = config["location"]
    mlflow.log_params({"data_identifier": data_identifier})
    logger.info("Getting dataset: %s", data_identifier)
    data = data_adaptor.get(data_identifier, location)
    logger.info(data)
    dataset = data_processor.process(data)

    return dataset


@op(
    required_resource_keys={"model_trainer"},
    out={"trained_model": Out()},
)
def train_model(context, model, data):
    logger = context.log
    config = context.op_config

    trainer = context.resources.model_trainer
    logger.info("Training")
    trained_model = trainer.train(model, data)
    logger.info(model_inputs)

    return trained_model


@op(
    required_resource_keys={"model_converter"},
    ins={"trained_model": In()},
)
def convert_model(context, trained_model, model_inputs):
    logger = context.log
    config = context.op_config

    logger.info(model_inputs)
    converter = context.resources.model_converter
    logger.info(f"Converting with {converter.converter.__class__.__name__}")
    converted_model = converter.convert(trained_model)

    return converted_model


# TODO: figure out how to generate op config
#   Answer: put an op_config key into the serviceconfig
#   and import that config, using the op config key for
#   the op config
@op(
    config_schema={"trained_model_identifier": str, "location": str},
    required_resource_keys={"save_model_model_repository"},
)
def save_model(context, model):
    logger = context.log
    config = context.op_config

    model_repository = context.resources.save_model_model_repository

    model_identifier = config["trained_model_identifier"]
    location = config["location"]
    logger.info("Saving model %s to %s", model_identifier, location)

    model_repository.put(model_identifier, location, model)
