from dagster import Field, Noneable, resource
from services.sklear_linear_regression_converter import \
    SKLearnLinearRegressionConverter

from infrastructure.model_converter import ModelConverter

ModelConverter.converters = {
    SKLearnLinearRegressionConverter.__name__: SKLearnLinearRegressionConverter
}


@resource(
    config_schema={
        "converter": str,
        **{
            converter_config_name: Field(
                Noneable(converter.resource_config.get_config())
            )
            for converter_config_name, converter in ModelConverter.converters.items()
        },
    }
)
def model_converter(init_context):
    config = init_context.resource_config

    converter_name = config["converter"]
    converter_override_config = config[converter_name]

    return ModelConverter(
        converter_name, override_init_config=converter_override_config
    )
