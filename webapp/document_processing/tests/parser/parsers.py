import io
import shlex
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from document_processing.parsers import (
    ParsedFile,
    ParsedFileCollection,
    ParserCoordinator,
    WordProcessorTextParser,
    WordProcessorXmlParser,
)


class TestFileParsers(unittest.TestCase):
    def test_FileParser(self):
        # TODO: Sort this out
        return True

    @patch("document_processing.parsers.subprocess")
    def test_WordProcessorXmlParser(self, mock_subprocess):
        original_filename = "original_filename.ext"
        mock_completed_process = Mock(args=[None, None, None, None, original_filename])
        mock_subprocess.run = Mock(return_value=mock_completed_process)

        parser = WordProcessorXmlParser()

        tf = Mock(name="some_name_we_dont_use_anywhere")
        command = shlex.split(
            f"soffice --headless --convert-to fodt:'OpenDocument Text Flat XML' {tf.name}"
        )

        result_filename = parser.process(tf)

        expected_filename = Path(
            "/backend" + "/" + original_filename.split(".")[0] + ".fodt"
        )
        assert result_filename == expected_filename
        mock_subprocess.run.assert_called_with(command)

    @patch("document_processing.parsers.subprocess")
    def test_WordProcessorTextParser(self, mock_subprocess):
        original_filename = "original_filename.ext"
        mock_completed_process = Mock(args=[None, None, None, None, original_filename])
        mock_subprocess.run = Mock(return_value=mock_completed_process)

        parser = WordProcessorTextParser()

        tf = Mock()
        tf.name = "some_name_we_dont_use_anywhere"

        command = shlex.split(f"soffice --headless --convert-to txt:Text {tf.name}")

        result_filename = parser.process(tf)

        expected_filename = Path(
            "/backend" + "/" + original_filename.split(".")[0] + ".txt"
        )
        assert result_filename == expected_filename
        mock_subprocess.run.assert_called_with(command)


class TestParserCoordinator(unittest.TestCase):
    @unittest.expectedFailure
    def test_parse(self):
        # TODO: this test and the unwritten one above indicate teh code needs to be refactored..
        # doing silly stuff down here
        parse_to_txt = ParsedFile(
            filename="test.txt", content=b"some bytes", file_extension="txt"
        )
        mock_parse_to_text_parse = Mock(return_value=parse_to_txt)
        mock_parser_to_text = Mock(
            parse=mock_parse_to_text_parse, allowed_types=["ext", "other"]
        )

        parse_to_fodt = ParsedFile(
            filename="test.fodt", content=b"some bytes", file_extension="fodt"
        )
        mock_parse_to_fodt_parse = Mock(return_value=parse_to_fodt)
        mock_parser_to_fodt = Mock(
            parse=mock_parse_to_fodt_parse, allowed_types=["ext", "other"]
        )

        mock_parsers = [mock_parser_to_text, mock_parser_to_fodt]

        coordinator = ParserCoordinator(mock_parsers)

        parsed_file_collection_data = {}
        datum1 = {"filename": "test.ext", "content": b"some bytes"}
        datum2 = {"filename": "test.other", "content": b"some other bytes"}

        parsed_file_collections = coordinator.parse([datum1, datum2])

        assert parsed_file_collections == [
            ParsedFileCollection(
                fodt=ParsedFile(
                    filename="test.fodt", content="some bytes", file_extension="fodt"
                ),
                txt=ParsedFile(
                    filename="test.txt", content="some bytes", file_extension="txt"
                ),
                original=ParsedFile(
                    filename="test.ext", content="some bytes", file_extension="ext"
                ),
            ),
            ParsedFileCollection(
                fodt=ParsedFile(
                    filename="test.fodt",
                    content="some other bytes",
                    file_extension="fodt",
                ),
                txt=ParsedFile(
                    filename="test.txt",
                    content="some other bytes",
                    file_extension="txt",
                ),
                original=ParsedFile(
                    filename="test.other",
                    content="some other bytes",
                    file_extension="other",
                ),
            ),
        ]

    def test__add_original_file_data(self):
        mock_parsers = [Mock()] * 3
        coordinator = ParserCoordinator(mock_parsers)

        parsed_file_collection_data = {}
        datum = {"filename": "test.ext", "content": b"some bytes"}

        parsed_file_collection_data = coordinator._add_original_file_data(
            parsed_file_collection_data, datum
        )

        assert parsed_file_collection_data["original"] == ParsedFile(
            file_extension="ext", filename="test.ext", content=b"some bytes"
        )


if __name__ == "__main__":
    unittest.main()
