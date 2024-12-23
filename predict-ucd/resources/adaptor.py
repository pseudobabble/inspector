from dagster import Field, Noneable, resource

from infrastructure.adaptor_clients.s3_client import S3Client
from infrastructure.data_adaptor import DataAdaptor

DataAdaptor.clients.update({S3Client.__name__: S3Client})


@resource(
    config_schema={
        "client": str,
        **{
            client_config_name: Field(Noneable(client.resource_config.get_config()))
            for client_config_name, client in DataAdaptor.clients.items()
        },
    }
)
def data_adaptor(init_context):
    config = init_context.resource_config

    print(config)

    client_name = config["client"]
    client_override_config = config[client_name]

    return DataAdaptor(client_name, override_init_config=client_override_config)
