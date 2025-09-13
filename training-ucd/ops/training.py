from dagster import Dict, Field, In, Out, String, op

from infrastructure.run_context import RunContext


@op(
    config_schema={
        "experiment_name": str,
        "experiment_description": str,
        "run_name": str,
    },
    required_resource_keys={"experiment_tracker"},
)
def start_experiment(context):
    logger = context.log
    config = context.op_config

    # Get the tracker
    tracker = context.resources.experiment_tracker

    # Get the experiment and run info
    experiment_name = config["experiment_name"]
    experiment_description = config["experiment_description"]
    run_name = config["run_name"]

    # Create the run context with initial information
    run_context = RunContext(
        experiment_name=experiment_name,
        experiment_description=experiment_description,
        run_name=run_name,
    )

    # Start or attach to the experiment
    # and add the experiment identifier to the run context
    experiment_id = tracker.create_experiment(run_context.experiment_name)
    run_context.experiment_id = experiment_id
    logger.info(f"Experiment {experiment_name} : {experiment_description} created")

    # Start the run and add the run id to the run context
    run_id = tracker.start_run(run_context.experiment_id, run_context.run_name)
    run_context.run_id = run_id
    logger.info(f"Run {run_name} {run_id} started")

    return run_context.to_dict()


@op(
    config_schema={"model_identifier": str, "model_location": str},
    required_resource_keys={"get_model_model_repository", "experiment_tracker"},
    ins={"run_context": In()},
)
def get_model(context, run_context):
    logger = context.log
    config = context.op_config

    model_repository = context.resources.get_model_model_repository
    tracker = context.resources.experiment_tracker

    # Deserialize RunContext
    run_context = RunContext.from_dict(run_context)

    logger.info(f"Experiment {run_context.experiment_id}, run {run_context.run_id}")

    model_identifier = config["model_identifier"]
    model_location = config["model_location"]
    logger.info("Getting model %s from location %s", model_identifier, model_location)
    model = model_repository.get(model_identifier, model_location)

    tracker.log_parameter(run_context.run_id, "test param", 1)

    return model


@op(
    config_schema={"data_identifier": str, "location": str},
    required_resource_keys={
        #        "mlflow",
        "data_adaptor",
        "data_processor",
        "experiment_tracker",
    },
    ins={"start": In()},
)
def get_data(context, start):
    config = context.op_config
    logger = context.log
    #    mlflow = context.resources.mlflow
    data_adaptor = context.resources.data_adaptor
    data_processor = context.resources.data_processor
    tracker = context.resources.experiment_tracker

    data_identifier = config["data_identifier"]
    location = config["location"]
    #    mlflow.log_params({'data_identifier': data_identifier})
    logger.info("Getting dataset: %s", data_identifier)
    data = data_adaptor.get(data_identifier, location)
    logger.info(data)
    dataset = data_processor.process(data)

    return dataset


@op(
    required_resource_keys={"model_trainer", "experiment_tracker"},
    out={"trained_model": Out(), "model_inputs": Out()},
)
def train_model(context, model, data):
    logger = context.log
    config = context.op_config

    trainer = context.resources.model_trainer
    tracker = context.resources.experiment_tracker

    logger.info("Training")
    trained_model, model_inputs = trainer.train(model, data)
    logger.info(model_inputs)

    return trained_model, model_inputs


@op(
    required_resource_keys={"model_converter", "experiment_tracker"},
    ins={"trained_model": In(), "model_inputs": In()},
)
def convert_model(context, trained_model, model_inputs):
    logger = context.log
    config = context.op_config

    logger.info(model_inputs)
    converter = context.resources.model_converter
    tracker = context.resources.experiment_tracker

    logger.info(f"Converting with {converter.converter.__class__.__name__}")
    converted_model = converter.convert(
        model=trained_model, input_types=model_inputs, logger=logger
    )

    return converted_model


@op(
    config_schema={"trained_model_identifier": str, "location": str},
    required_resource_keys={"save_model_model_repository", "experiment_tracker"},
)
def save_model(context, model):
    logger = context.log
    config = context.op_config

    model_repository = context.resources.save_model_model_repository
    tracker = context.resources.experiment_tracker

    model_identifier = config["trained_model_identifier"]
    location = config["location"]
    logger.info("Saving model %s to %s", model_identifier, location)

    model_repository.put(model_identifier, location, model)
