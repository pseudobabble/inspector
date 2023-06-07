import io
from dataclasses import dataclass
from typing import Any

from minio import Minio

from infrastructure.data_adaptor import Adaptor
from infrastructure.service import ServiceConfig


@dataclass
class S3AdaptorConfig(ServiceConfig):
    host: str
    port: str
    access_key: str
    secret_key: str
    bucket_name: str


class S3Client(Adaptor):
    resource_config = S3AdaptorConfig

    def __init__(self, config: S3AdaptorConfig = None):
        config = config or S3AdaptorConfig.from_env()
        self.vendor_client = Minio(
            endpoint=f"{config.host}:{config.port}",
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=False,
        )
        self.bucket_name = config.bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.vendor_client.bucket_exists(self.bucket_name):
            self.vendor_client.make_bucket(self.bucket_name)

    def put(self, filename: str, directory: str, value: Any, *args, **kwargs):
        key = f"{directory}/{filename}"
        try:
            serialised_value = io.BytesIO(value)
            response = self.vendor_client.put_object(
                self.bucket_name,
                key,
                serialised_value,
                length=-1,
                part_size=10 * 1024 * 1024,
            )
            # TODO: error handling by status code
            return response
        except Exception as e:  # TODO: fix this
            raise e

    def get(self, filename: str, directory: str, *args, **kwargs):
        key = f"{directory}/{filename}"
        try:
            response = self.vendor_client.get_object(self.bucket_name, key)
            retrieved_object = io.BytesIO(response.data)
            response.close()
            response.release_conn()
            return retrieved_object
        except Exception as e:
            raise e
