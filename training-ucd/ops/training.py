from dagster import op


@op(
    config_schema={
        'model_identifier': str
        'model_class_name': str
    },
    required_resource_keys={
        "hf_model_repository"
    }
)
def get_pretrained_model(context):
    logger = context.log
    config = context.op_config

    model_repository = context.resources.model_repository

    model_identifier = config['model_identifier']
    model_class_name = config['model_class_name']
    logger.info(
        'Getting pretrained model %s for class %s',
        model_identifier,
        model_class_name
    )
    model = model_repository.get(model_identifier, model_class_name)

    return model


@op(
    config_schema={
        'data_identifier': str,
        'destination_format': str
    },
    required_resource_keys={
        "data_adaptor"
        "data_processor"
    }
)
def get_data(context):
    config = context.op_config
    logger = context.log
    data_adaptor = context.resources.data_adaptor
    data_processor = context.resources.data_processor

    data_identifier = config['data_identifier']
    destination_format = config['destination_format']
    logger.info('Getting dataset: %s', data_identifier)
    data = data_adaptor.get(data_identifier)
    dataset = data_processor.process(data)

    return dataset

@op(
    required_resource_keys={
        "trainer"
    }
)
def train_pretrained_model(model, data):
    logger = context.log
    config = context.op_config

    trainer = context.resources.trainer
    logger.info('Training')
    trained_model = trainer.train(model, data)

    return trained_model

@op(
    config_schema={'trained_model_identifier': str}
    required_resource_keys={
        "s3_model_repository"
    }
)
def save_model(context):
    logger = context.log
    config = context.op_config

    model_repository = context.resources.model_repository

    model_identifier = config['trained_model_identifier']
    logger.info('Saving model: %s', model_identifier)

    model.save_pretrained(trained_model_identifier, save_function=model_repository.put)
