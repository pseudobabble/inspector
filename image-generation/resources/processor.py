from dagster import resource, Field, Noneable

from infrastructure import (
    DataProcessor
)


@resource(
    config_schema={
        "processor": str,
        **{processor_config_name: Field(
            Noneable(
                processor.resource_config.get_config()
            )
        )
           for processor_config_name, processor
           in DataProcessor.processors.items()}
    }
)
def data_processor(init_context):
    config = init_context.resource_config

    processor_name = config["processor"]
    processor_override_config = config[processor_name]

    return DataProcessor(
        processor_name,
        override_init_config=processor_override_config
    )
