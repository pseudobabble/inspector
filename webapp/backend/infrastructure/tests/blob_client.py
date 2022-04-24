import unittest
from unittest.mock import Mock
from infrastructure.blob_client import MinioBlobClient


class TestMinioBlobClient(unittest.TestCase):

    def test_get(self):
        mock_minio = Mock()

        original_value = {'some': b'dict'}
        mock_loads = Mock(return_value=original_value)
        mock_dumps = Mock(return_value=b'some bytes')
        mock_serializer = Mock(loads=mock_loads, dumps=mock_dumps)

        mock_response = Mock(
            close=Mock(),
            release_conn=Mock(),
            read=Mock(return_value=b'some bytes')
        )
        mock_get_object = Mock(return_value=mock_response)
        mock_minio.get_object = mock_get_object


        blob_client = MinioBlobClient(
            vendor_client=mock_minio,
            bucket_name='test',
            serializer=mock_serializer
        )

        parsed_file_collection = blob_client.get('test key')

        assert parsed_file_collection == original_value
        mock_minio.get_object.assert_called_with('test', 'test key')
        mock_serializer.loads.assert_called_with(b'some bytes')
        mock_response.close.assert_called()
        mock_response.release_conn.assert_called()

    def test_put(self):
        mock_minio = Mock()

        original_value = {'some': b'dict'}
        mock_loads = Mock(return_value=original_value)
        mock_dumps = Mock(return_value=b'some bytes')
        mock_serializer = Mock(loads=mock_loads, dumps=mock_dumps)

        mock_response = Mock()
        mock_put_object = Mock(return_value=mock_response)
        mock_minio.put_object = mock_put_object


        blob_client = MinioBlobClient(
            vendor_client=mock_minio,
            bucket_name='test',
            serializer=mock_serializer
        )

        response = blob_client.put('test key', original_value)

        assert response == mock_response
        mock_serializer.dumps.assert_called_with(original_value)
        mock_minio.put_object.assert_called_with('test', 'test key', b'some bytes', length=-1, part_size=10*1024*1024)

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
