import unittest
from unittest.mock import Mock, patch
import io
import shlex
import tempfile

from document_processing.parsers import WordProcessorXmlParser, WordProcessorTextParser, ParsedFile


class TestFileParsers(unittest.TestCase):

    @patch('document_processing.parsers.subprocess')
    def test_WordProcessorXmlParser(self, mock_subprocess):
        original_filename = 'original_filename.ext'
        mock_completed_process = Mock(args=[None, None, None, None, original_filename])
        mock_subprocess.run = Mock(return_value=mock_completed_process)

        parser = WordProcessorXmlParser()

        tf = Mock(name='some_name_we_dont_use_anywhere')
        command = shlex.split(
            f"soffice --headless --convert-to fodt:'OpenDocument Text Flat XML' {tf.name}"
        )

        result_filename = parser.process(tf)

        assert result_filename == original_filename.split('.')[0] + '.fodt'
        mock_subprocess.run.assert_called_with(command)



class TestParserCoordinator(unittest.TestCase):

    def test_parse(self):
        assert True


if __name__ == '__main__':
    unittest.main()
