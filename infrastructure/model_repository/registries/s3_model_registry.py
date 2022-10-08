import io
from dataclasses import dataclass

from infrastructure.model_repository import (
    ModelRepositoryConfig,
    ModelRepository
)

from minio import Minio


@dataclass
class S3ModelRepositoryConfig(ModelRepositoryConfig):
    host: str
    port: str
    access_key: str
    secret_key: str
    bucket_name: str


class S3ModelRepository(ModelRepositoryConfig):

    host: str = None
    port: str = None
    access_key: str
    secret_key: str
    bucket_name: str

    def __init__(config: S3ModelRepositoryConfig):
        self.vendor_client = Minio(
            endpoint=f"{config.host}:{config.port}",
            access_key=config.access_key,
            secret_key=config.secret_key,
        )
        self.bucket = config.bucket
        self._ensure_bucket_exists()
        super().__init__(config)

    def _ensure_bucket_exists(self):
        if not self.vendor_client.bucket_exists(self.bucket_name):
            self.vendor_client.make_bucket(self.bucket_name)

    def put(self, model_filename: str, directory: str, value: Any, *args, **kwargs):
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

    def get(self, model_identifier: str, location: str, *args, **kwargs):
        key = f"{directory}/{filename}"
        try:
            response = self.vendor_client.get_object(self.bucket_name, key)
            # TODO: add error handling
            retrieved_object = io.BytesIO(response.data)
            return retrieved_object
        finally:
            response.close()
            response.release_conn()
