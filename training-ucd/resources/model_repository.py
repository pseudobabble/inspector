from dagster import resource

from infrastructure.model_repository import (
    ModelRepository
)


@resource(
    config_schema={
        "registry": str,
        registry_config_name: Field(
            Noneable(
                registry.config.get_resource_config()
            )
        )
        for registry_config_name, registry
        in ModelRepository.registries.items()
    }
)
def (init_context):
    config = init_context.resource_config

    registry_name = config["registry"]
    registry_override_config = config[registry_name]

    return ModelRepository(registry_name, override_init_config=registry_override_config)
