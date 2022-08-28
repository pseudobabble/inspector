import io
import pickle
from dataclasses import dataclass

from minio import Minio


@dataclass
class MinioConnectionParams:
    host: str
    port: str
    access_key: str
    secret_key: str
    bucket_name: str


class MinioBlobClient:
    def __init__(
        self, url, access_key, secret_key, bucket_name, secure=False, serializer=pickle
    ):
        self.vendor_client = Minio(
            url, access_key=access_key, secret_key=secret_key, secure=secure
        )
        self.bucket_name = bucket_name
        self.serializer = serializer
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.vendor_client.bucket_exists(self.bucket_name):
            self.vendor_client.make_bucket(self.bucket_name)

    def put(self, key, value):
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

    def get(self, key):
        try:
            response = self.vendor_client.get_object(self.bucket_name, key)
            # TODO: add error handling
            retrieved_object = io.BytesIO(response.data)
            return retrieved_object
        finally:
            response.close()
            response.release_conn()
