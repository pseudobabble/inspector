from dagster import resource

from services.model.hf_model_repository import (
    HFModelRepository,
    HFModelRepositoryConfig
)
from services.model.s3_model_repository import (
    S3ModelRepository,
    S3ModelRepositoryConfig
)


@resource(config_schema=HFModelRepositoryConfig.get_resource_config())
def hf_model_repository(init_context):
    hf_config = HFModelRepositoryConfig.from_dict(init_context)
    return HFModelRepository.configure(hf_config)


@resource(config_schema=S3ModelRepositoryConfig.get_resource_config())
def s3_model_repository(init_context):
    s3_config = S3RepositoryConfig.from_dict(init_context)
    return S3ModelRepository.configure(s3_config)
