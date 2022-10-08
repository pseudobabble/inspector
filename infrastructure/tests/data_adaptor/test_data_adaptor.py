from unittest import TestCase
from unittest.mock import patch, Mock, PropertyMock

from infrastructure.data_adaptor.data_adaptor import DataAdaptor


class TestDataAdaptor(TestCase):

    def test___init__default(self):
        mock_client_class = Mock()
        with patch.object(DataAdaptor, 'clients', {'some client': mock_client_class}):
            adaptor = DataAdaptor('some client')

            mock_client_class.assert_called()


    def test___init__override(self):

        override_config = {'host': 'a', 'port': 'b', 'access_key': 'c', 'secret_key': 'd', 'bucket_name': 'e'}

        mock_client_config_instance = Mock(**override_config)
        mock_from_dict = Mock(return_value=mock_client_config_instance)
        mock_client_config_class = Mock(from_dict=mock_from_dict)
        mock_client_class = Mock(resource_config=mock_client_config_class)

        with patch.object(DataAdaptor, 'clients', {'some client': mock_client_class}):
            adaptor = DataAdaptor('some client', override_init_config=override_config)

            mock_client_class.assert_called_once_with(mock_client_config_instance)

    def test_get(self):
        mock_get_result = Mock()
        mock_get = Mock(return_value=mock_get_result)
        mock_client_instance = Mock(get=mock_get)
        mock_client_class = Mock(return_value=mock_client_instance)
        with patch.object(DataAdaptor, 'clients', {'some_client': mock_client_class}):
            adaptor = DataAdaptor('some_client')
            adaptor.get('some identifier', 'some location', 'a random 3rd', fourth=True)

            mock_get.assert_called_once_with('some identifier', 'some location', 'a random 3rd', fourth=True)


    def test_put(self):
        mock_put_result = Mock()
        mock_put = Mock(return_value=mock_put_result)
        mock_client_instance = Mock(put=mock_put)
        mock_client_class = Mock(return_value=mock_client_instance)
        with patch.object(DataAdaptor, 'clients', {'some_client': mock_client_class}):
            adaptor = DataAdaptor('some_client')
            adaptor.put('some identifier', 'some location', 'a random 3rd', fourth=True)

            mock_put.assert_called_once_with('some identifier', 'some location', 'a random 3rd', fourth=True)
