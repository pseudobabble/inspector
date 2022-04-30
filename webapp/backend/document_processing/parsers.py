"""
This module contains classes for parsing various file formats into more useful forms,
usually text extraction, maybe xml conversion, etc
"""
from typing import Dict, List, Any, Union, Optional
from abc import abstractmethod
import shlex
import subprocess
from tempfile import NamedTemporaryFile
from pathlib import Path
import os

from pydantic import BaseModel


class ParsedFile(BaseModel):
    filename: str
    content: Union[str, bytes]
    file_extension: str


class ParsedFileCollection(BaseModel):
    fodt: ParsedFile
    txt: ParsedFile
    original: ParsedFile



class FileParser:

    allowed_types = NotImplementedError()

    @abstractmethod
    def process(self, temporary_file: NamedTemporaryFile) -> str:
        raise NotImplementedError()

    def parse(self, file_datum: Dict[str, Any]) -> ParsedFile:

        content = file_datum['content']

        original_filename_stem = Path(file_datum['filename']).stem

        with NamedTemporaryFile() as tf:
            tf.write(content)

            result_filename = self.process(tf)
            result_filename_extension = Path(result_filename).suffix

            original_filename_stem_with_new_extension = original_filename_stem + result_filename_extension

            parsed_file = self._parse_temp_file(result_filename, original_filename_stem_with_new_extension)

            return parsed_file

    def _parse_temp_file(self, result_filename: str, filename: str):
        with open(result_filename, 'r') as tmp_file:
            parsed_file = ParsedFile(**{
                'filename': filename,
                'content': tmp_file.read(),
                'file_extension': Path(result_filename).suffix.replace('.', '')
            })
        # TODO: remove file

        return parsed_file


class WordProcessorXmlParser(FileParser):

    allowed_types = ['docx', 'doc', 'odt']

    def process(self, temporary_file: NamedTemporaryFile) -> str:
        result = subprocess.run(
            shlex.split(f"soffice --headless --convert-to fodt:'OpenDocument Text Flat XML' {temporary_file.name}")
        )

        result_filename = Path(result.args[4].split('.')[0] + '.fodt').name
        new_path = Path('/backend').joinpath(result_filename)

        return new_path


class WordProcessorTextParser(FileParser):

    allowed_types = ['docx', 'doc', 'odt']

    def process(self, temporary_file: NamedTemporaryFile) -> str:
        result = subprocess.run(
            shlex.split(f'soffice --headless --convert-to txt:Text {temporary_file.name}')
        )

        result_filename = Path(result.args[4].split('.')[0] + '.txt').name
        new_path = Path('/backend').joinpath(result_filename)

        return new_path


class ParserCoordinator:

    def __init__(self, parsers: Optional[List[FileParser]] = None):
        self.parsers = parsers or [
            WordProcessorXmlParser(),
            WordProcessorTextParser()
        ]

    def set_parser(self, parser: FileParser) -> None:
        self.parsers.append(parser())

    def parse(self, uploaded_file_data: List[dict]) -> List[ParsedFileCollection]:
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

    def _add_original_file_data(self, parsed_file_collection_data: dict, datum: dict):
        original_file_extension = Path(datum['filename']).suffix.replace('.', '')
        original_file_data = {**datum, "file_extension": original_file_extension}
        parsed_file_collection_data['original'] = ParsedFile(**original_file_data)

        return parsed_file_collection_data
