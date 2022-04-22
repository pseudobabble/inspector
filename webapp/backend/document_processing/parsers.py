"""
This module contains classes for parsing various file formats into more useful forms,
usually text extraction, maybe xml conversion, etc
"""
from typing import Dict, List, Any, Union
from abc import abstractmethod
import shlex
import subprocess
from tempfile import NamedTemporaryFile
from pathlib import Path

from pydantic import BaseModel


class ParsedFile(BaseModel):
    filename: str
    content: Union[str, bytes]
    file_extension: str


class ParsedFileCollection(BaseModel):
    fodt: ParsedFile
    text: ParsedFile
    original: ParsedFile



class FileParser:

    allowed_types = NotImplementedError()

    @abstractmethod
    def process(temporary_file: NamedTemporaryFile) -> str:
        raise NotImplementedError()

    def parse(file_datum: Dict[str, Any]) -> ParsedFile:

        content = file_datum['content']

        original_filename_path = Path(file_datum['filename'])
        original_filename_stem = original_filename_path.stem

        with NamedTemporaryFile() as tf:
            tf.write(content)

            result_filename = self.process(tf)
            result_filename_extension = Path(result_filename).suffix

            original_filename_stem_with_new_extension = original_filename_stem + result_filename_extension

            parsed_file = self._parse_temp_file(result_filename, original_filename_stem_with_new_extension)

            return parsed_file

    def _parse_temp_file(result_filename: str, filename: str):
        with open(result_filename, 'r') as tmp_file:
            parsed_file = ParsedFile(**{
                'filename': filename,
                'content': tmp_file.read(),
                'file_extension': result_filename_extension
            })

        return parsed_file


class WordProcessorXmlParser(FileParser):

    allowed_types = ['docx', 'doc', 'odt']

    def process(temporary_file: NamedTemporaryFile) -> str:
        result = subprocess.run(
            shlex.split(f"soffice --headless --convert-to fodt:'OpenDocument Text Flat XML' {tf.temporary_file}")
        )

        result_filename = result.args[4] + '.fodt'

        return result_filename


class WordProcessorTextParser(FileParser):

    allowed_types = ['docx', 'doc', 'odt']

    def process(temporary_file: NamedTemporaryFile) -> str:
        result = subprocess.run(
            shlex.split(f"soffice --headless --convert-to txt:Text {tf.temporary_file}'")
        )

        result_filename = result.args[4] + '.txt'

        return result_filename


class ParserCoordinator:

    def __init__(self, parsers: Optional[List[FileParser]] = None):
        self.parsers = parsers or [WordProcessorXmlParser(), WordProcessorTextParser()]

    def set_parser(parser: FileParser) -> None:
        self.parsers.append(parser())

    def parse(uploaded_file_data: List[dict]) -> List[ParsedFileCollection]:
        parsed_file_collections = []
        for datum in uploaded_file_data:
            parsed_file_collection = self._add_original_file_data({}, datum)

            for parser in self.parsers:
                original_file_key = Path(datum['filename']).suffix.replace('.', '')
                if original_file_key in parser.allowed_types:
                    parsed_file = parser.parse(datum)
                    collection_key = parsed_file.file_extension.replace('.', '')
                    parsed_file_collection[collection_key] = parsed_file

            parsed_file_collections.append(
                ParsedFileCollection(**parsed_file_collection)
            )

        return parsed_file_collections

    def _add_original_file_data(parsed_file_collection_data: dict, datum: dict):
        original_file_key = Path(datum['filename']).suffix.replace('.', '')
        original_file_data = {**datum, "file_extension": original_file_key}
        parsed_file_collection[original_file_key] = ParsedFile(**original_file_data)

        return parsed_file_collection
