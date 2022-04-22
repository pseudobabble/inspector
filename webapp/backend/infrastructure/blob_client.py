import os
from abc import abstractmethod

from minio import Minio
from minio.error import S3Error


class BlobClient:

    def __init__(self, *args, **kwargs):
        self._ensure_bucket_exists()

    @abstractmethod
    def _ensure_bucket_exists(self):
        raise NotImplementedError()

    @abstractmethod
    def put(self, key, value):
        raise NotImplementedError()

    @abstractmethod
    def get(self, key):
        raise NotImplementedError()


class MinioBlobClient:

    def __init__(
            self,
            vendor_client=Minio(
                'inspector-mlflow-s3-1:9000',
                access_key=os.getenv('AWS_ACCESS_KEY_ID'),
                secret_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            ),
            bucket_name=os.getenv('AWS_BUCKET_NAME')
    ):
        self.vendor_client = vendor_client
        self.bucket_name = bucket_name
        super().__init__()

    def _ensure_bucket_exists(self):
        if not self.vendor_client.bucket_exists(self.bucket_name):
            self.vendor_client.make_bucket(self.bucket_name)


    def put(self, key, value):
        try:
            response = self.vendor_client.fput_object(
                self.bucket_name,
                key,
                value
            )
            return response
        except Exception as e: # TODO: fix this
            raise e

    def get(self, key):
        try:
            response = self.vendor_client.get_object(self.bucket_name, key)
            return response
        finally:
            response.close()
            response.release_conn()
