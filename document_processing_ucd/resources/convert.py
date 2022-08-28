from dagster import resource

from adaptors.convert.tika_client import TikaClient, TikaConnectionParams

@resource(config_schema={'host': str, 'port': str, 'endpoint': str})
def tika_client(init_context):
    connection_params = TikaConnectionParams(
        host=init_context.resource_config['host'],
        port=init_context.resource_config['port'],
        endpoint=init_context.resource_config['endpoint']
    )

    return TikaClient(connection_params=connection_params)
