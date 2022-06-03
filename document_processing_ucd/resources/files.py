from adaptors import BlobClient, Parser
from dagster import resource


@resource(
    config_schema={"url": str, "access_key": str, "secret_key": str, "bucket_name": str}
)
def blob_client(init_context):
    url = init_context.resource_config["url"]
    access_key = init_context.resource_config["access_key"]
    secret_key = init_context.resource_config["secret_key"]
    bucket_name = init_context.resource_config["bucket_name"]

    # TODO: make blob client selectable
    return BlobClient(
        url, access_key=access_key, secret_key=secret_key, bucket_name=bucket_name
    )


@resource
def file_parser(init_context):
    return Parser()
