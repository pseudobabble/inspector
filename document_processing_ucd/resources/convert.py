from dagster import resource

from adaptors.convert.tika_client import TikaClient, TikaConnectionParams

@resource(config_schema={'host': str, 'port': str})
def tika_client(init_context):
    connection_params = TikaConnectionParams(
        host=init_context.host,
        port=init_context.port
    )

    return TikaClient(connection_params=connection_params)
