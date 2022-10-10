from unittest import TestCase
from unittest.mock import patch, Mock, PropertyMock

from infrastructure.data_trainer.data_trainer import ModelTrainer


class TestModelTrainer(TestCase):

    def test___init__default(self):
        mock_trainer_class = Mock()
        with patch.object(ModelTrainer, 'trainers', {'some trainer': mock_trainer_class}):
            trainer = ModelTrainer('some trainer')

            mock_trainer_class.assert_called()


    def test___init__override(self):

        override_config = {'host': 'a', 'port': 'b', 'access_key': 'c', 'secret_key': 'd', 'bucket_name': 'e'}

        mock_trainer_config_instance = Mock(**override_config)
        mock_from_dict = Mock(return_value=mock_trainer_config_instance)
        mock_trainer_config_class = Mock(from_dict=mock_from_dict)
        mock_trainer_class = Mock(resource_config=mock_trainer_config_class)

        with patch.object(ModelTrainer, 'trainers', {'some trainer': mock_trainer_class}):
            trainer = ModelTrainer('some trainer', override_init_config=override_config)

            mock_trainer_class.assert_called_once_with(mock_trainer_config_instance)

    def test_process(self):
        mock_process_result = Mock()
        mock_process = Mock(return_value=mock_process_result)
        mock_trainer_instance = Mock(process=mock_process)
        mock_trainer_class = Mock(return_value=mock_trainer_instance)
        with patch.object(ModelTrainer, 'trainers', {'some_trainer': mock_trainer_class}):
            trainer = ModelTrainer('some_trainer')
            trainer.process('some identifier', 'some location', 'a random 3rd', fourth=True)

            mock_process.assert_called_once_with('some identifier', 'some location', 'a random 3rd', fourth=True)
