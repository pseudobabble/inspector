import unittest
from unittest.mock import Mock
from infrastructure.blob_client import MinioBlobClient


class TestMinioBlobClient(unittest.TestCase):

    def test_get(self):
        mock_minio = Mock()

        mock_response = Mock(
            close=Mock(),
            release_conn=Mock()
        )
        mock_get_object = Mock(return_value=mock_response)
        mock_minio.get_object = mock_get_object


        blob_client = MinioBlobClient(
            vendor_client=mock_minio,
            bucket_name='test'
        )

        response = blob_client.get('test key')

        assert response == mock_response
        mock_get_object.assert_called_with('test', 'test key')
        mock_response.close.assert_called()
        mock_response.release_conn.assert_called()

    def test_put(self):
        mock_minio = Mock()

        mock_response = Mock()
        mock_fput_object = Mock(return_value=mock_response)
        mock_minio.fput_object = mock_fput_object


        blob_client = MinioBlobClient(
            vendor_client=mock_minio,
            bucket_name='test'
        )

        response = blob_client.put('test key', {'test': None})

        assert response == mock_response
        mock_fput_object.assert_called_with('test', 'test key', {'test': None})

    def test__ensure_bucket_exists(self):
        mock_minio = Mock()

        mock_bucket_exists = Mock(return_value=False)
        mock_minio.bucket_exists = mock_bucket_exists
        mock_make_bucket = Mock()
        mock_minio.make_bucket = mock_make_bucket


        blob_client = MinioBlobClient(
            vendor_client=mock_minio,
            bucket_name='test'
        )

        blob_client._ensure_bucket_exists()

        mock_bucket_exists.assert_called_with('test')
        mock_make_bucket.assert_called_with('test')

    def test__init__(self):
        mock_minio = Mock()

        mock_bucket_exists = Mock(return_value=False)
        mock_minio.bucket_exists = mock_bucket_exists
        mock_make_bucket = Mock()
        mock_minio.make_bucket = mock_make_bucket


        blob_client = MinioBlobClient(
            vendor_client=mock_minio,
            bucket_name='test'
        )

        assert blob_client.vendor_client == mock_minio
        assert blob_client.bucket_name == 'test'


    # How to check that super().__init__ calls _ensure_bucket_exists



if __name__ == "__main__":
    unittest.main()
