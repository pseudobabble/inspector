import os
from abc import abstractmethod
import pickle
import io

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
            url,
            access_key,
            secret_key,
            bucket_name,
            secure=False,
            serializer=pickle
    ):
        self.vendor_client = Minio(
            url,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket_name = bucket_name
        self.serializer = serializer
        self._ensure_bucket_exists()
        super().__init__()

    def _ensure_bucket_exists(self):
        if not self.vendor_client.bucket_exists(self.bucket_name):
            self.vendor_client.make_bucket(self.bucket_name)

    def put(self, key, value):
        try:
            serialised_value = io.BytesIO(self.serializer.dumps(value))
            response = self.vendor_client.put_object(
                self.bucket_name,
                key,
                serialised_value,
                length=-1,
                part_size=10*1024*1024
            )
            # TODO: error handling by status code
            return response
        except Exception as e: # TODO: fix this
            raise e

    def get(self, key):
        try:
            response = self.vendor_client.get_object(self.bucket_name, key)
            # TODO: add error handling
            retrieved_object = self.serializer.loads(response.read())
            return retrieved_object
        finally:
            response.close()
            response.release_conn()
