from unittest import TestCase
from unittest.mock import patch, Mock, PropertyMock

from infrastructure.model_repository.model_repository import ModelRepository


class TestModelRepository(TestCase):

    def test___init__default(self):
        mock_registry_class = Mock()
        with patch.object(ModelRepository, 'registries', {'some registry': mock_registry_class}):
            adaptor = ModelRepository('some registry')

            mock_registry_class.assert_called()


    def test___init__override(self):

        override_init_config = {'some': 'value'}
        mock_registry_config_instance = Mock(**override_init_config)
        mock_from_dict = Mock(return_value=mock_registry_config_instance)
        mock_registry_config_class = Mock(from_dict=mock_from_dict)
        mock_registry_class = Mock(resource_config=mock_registry_config_class)

        with patch.object(ModelRepository, 'registries', {'some registry': mock_registry_class}):
            adaptor = ModelRepository('some registry', override_init_config=override_init_config)

            mock_registry_class.assert_called_once_with(mock_registry_config_instance)

    def test_get(self):
        mock_get_result = Mock()
        mock_get = Mock(return_value=mock_get_result)
        mock_registry_instance = Mock(get=mock_get)
        mock_registry_class = Mock(return_value=mock_registry_instance)
        with patch.object(ModelRepository, 'registries', {'some_registry': mock_registry_class}):
            adaptor = ModelRepository('some_registry')
            adaptor.get('some identifier', 'some location', 'a random 3rd', fourth=True)

            mock_get.assert_called_once_with('some identifier', 'some location', 'a random 3rd', fourth=True)


    def test_put(self):
        mock_put_result = Mock()
        mock_put = Mock(return_value=mock_put_result)
        mock_registry_instance = Mock(put=mock_put)
        mock_registry_class = Mock(return_value=mock_registry_instance)
        with patch.object(ModelRepository, 'registries', {'some_registry': mock_registry_class}):
            adaptor = ModelRepository('some_registry')
            adaptor.put('some identifier', 'some location', 'a random 3rd', fourth=True)

            mock_put.assert_called_once_with('some identifier', 'some location', 'a random 3rd', fourth=True)
