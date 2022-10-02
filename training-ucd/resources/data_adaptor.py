from dagster import resource

from services.data_adaptors.s3_adaptor import (
    S3Adaptor,
    S3AdaptorConfig
)


@resource(config_schema=S3AdaptorConfig.get_resource_config())
def s3_data_adaptor(init_context):
    s3_config = S3AdaptorConfig.from_dict(init_context)
    return S3Adaptor.configure(s3_config)
