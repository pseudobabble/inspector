from unittest import TestCase
from unittest.mock import patch, Mock, PropertyMock

from infrastructure.data_processor.data_processor import DataProcessor


class TestDataProcessor(TestCase):

    def test___init__default(self):
        mock_processor_class = Mock()
        with patch.object(DataProcessor, 'processors', {'some processor': mock_processor_class}):
            processor = DataProcessor('some processor')

            mock_processor_class.assert_called()


    def test___init__override(self):

        override_config = {'host': 'a', 'port': 'b', 'access_key': 'c', 'secret_key': 'd', 'bucket_name': 'e'}

        mock_processor_config_instance = Mock(**override_config)
        mock_from_dict = Mock(return_value=mock_processor_config_instance)
        mock_processor_config_class = Mock(from_dict=mock_from_dict)
        mock_processor_class = Mock(resource_config=mock_processor_config_class)

        with patch.object(DataProcessor, 'processors', {'some processor': mock_processor_class}):
            processor = DataProcessor('some processor', override_init_config=override_config)

            mock_processor_class.assert_called_once_with(mock_processor_config_instance)

    def test_process(self):
        mock_process_result = Mock()
        mock_process = Mock(return_value=mock_process_result)
        mock_processor_instance = Mock(process=mock_process)
        mock_processor_class = Mock(return_value=mock_processor_instance)
        with patch.object(DataProcessor, 'processors', {'some_processor': mock_processor_class}):
            processor = DataProcessor('some_processor')
            processor.process('some identifier', 'some location', 'a random 3rd', fourth=True)

            mock_process.assert_called_once_with('some identifier', 'some location', 'a random 3rd', fourth=True)
