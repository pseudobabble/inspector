from dagster import Field, Noneable, resource
from services.registries.sklearn_model_registry import SKLearnModelRegistry

from infrastructure import ModelRepository
from infrastructure.registries.s3_model_registry import S3ModelRegistry

ModelRepository.registries.update({SKLearnModelRegistry.__name__: SKLearnModelRegistry})
ModelRepository.registries.update({S3ModelRegistry.__name__: S3ModelRegistry})


@resource(
    config_schema={
        "registry": str,
        **{
            registry_config_name: Field(Noneable(registry.resource_config.get_config()))
            for registry_config_name, registry in ModelRepository.registries.items()
        },
    }
)
def model_repository(init_context):
    config = init_context.resource_config

    registry_name = config["registry"]
    registry_override_config = config[registry_name]

    return ModelRepository(registry_name, override_init_config=registry_override_config)
