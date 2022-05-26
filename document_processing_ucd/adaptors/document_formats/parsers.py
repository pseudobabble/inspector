"""
This module contains classes for parsing various file formats
into more useful forms,usually text extraction, maybe xml
conversion, etc
"""
import os
import shlex
import subprocess
from abc import abstractmethod
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List, Optional, Union

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

    def parse(self, file_datum: Dict[str, Any], logger) -> ParsedFile:

        content = file_datum["content"]

        original_filename_stem = Path(file_datum["filename"]).stem

        temp_file_path = Path(f'/tmp/{file_datum["filename"]}')
        with open(temp_file_path, "wb") as tf:
            logger.info("%s", tf.name)
            tf.write(content.encode("utf-8"))

        logger.info("52: /tmp contents: %s", os.listdir("/tmp"))
        result_filename = self.process(temp_file_path, logger)
        logger.info("54: /tmp contents: %s", os.listdir("/tmp"))
        # TODO: delete file
        logger.info("%s", result_filename)

        result_filename_extension = Path(result_filename).suffix
        original_filename_stem_with_new_extension = (
            original_filename_stem + result_filename_extension
        )

        logger.info(
            "61: BEFORE: /tmp contents: %s\nresult_filename: %s",
            os.listdir("/tmp"),
            result_filename,
        )
        parsed_file = self._parse_temp_file(
            result_filename, original_filename_stem_with_new_extension, logger
        )

        return parsed_file

    def _parse_temp_file(self, result_filename: str, filename: str, logger):
        logger.info(
            "68: JUST BEFORE: /tmp contents: %s\nresult_filename: %s",
            os.listdir("/tmp"),
            result_filename,
        )
        with open(result_filename, "r") as tmp_file:
            parsed_file = ParsedFile(
                **{
                    "filename": filename,
                    "content": tmp_file.read(),
                    "file_extension": Path(result_filename).suffix.replace(".", ""),
                }
            )
        # TODO: remove file

        return parsed_file


class WordProcessorXmlParser(FileParser):

    allowed_types = ["docx", "doc", "odt"]

    def process(self, temporary_file_path: Path, logger) -> str:
        outdir = temporary_file_path.parent
        os.listdir(outdir)
        # result = subprocess.run(
        #     shlex.split(
        #         f"soffice --headless --convert-to fodt:'OpenDocument"
        #         f"Text Flat XML' {temporary_file_path} --outdir {outdir}"
        #     ),
        #     capture_output=True
        # )
        result = subprocess.run(
            shlex.split("pwd && ls /tmp"), shell=True, capture_output=True
        )
        logger.info("%s", result)

        new_path = temporary_file_path.with_suffix(".fodt")

        return new_path


class WordProcessorTextParser(FileParser):

    allowed_types = ["docx", "doc", "odt"]

    def process(self, temporary_file_path: Path, logger) -> str:
        outdir = temporary_file_path.parent
        logger.info("102: BEFORE: outdir %s contents: %s", outdir, os.listdir(outdir))

        result = subprocess.run(shlex.split("ls /tmp"), shell=True, capture_output=True)
        logger.info("%s", result)

        result = subprocess.run(
            shlex.split(
                "soffice --headless --convert-to txt:Text"
                f" {temporary_file_path} --outdir {outdir}"
            ),
            shell=True,
        )
        logger.info("107: AFTER: outdir %s contents: %s", outdir, os.listdir(outdir))
        logger.info("result %s", result)

        new_path = temporary_file_path.with_suffix(".txt")

        return new_path


class ParserCoordinator:
    def __init__(self, parsers: Optional[List[FileParser]] = None):
        self.parsers = parsers or [
            WordProcessorTextParser(),
            #            WordProcessorXmlParser()
        ]

    def set_parser(self, parser: FileParser) -> None:
        self.parsers.append(parser())

    def parse(
        self, uploaded_file_data: List[dict], logger
    ) -> List[ParsedFileCollection]:
        parsed_file_collections = []
        for datum in uploaded_file_data:
            parsed_file_collection = self._add_original_file_data({}, datum)

            logger.info("%s", parsed_file_collection)
            for parser in self.parsers:
                original_file_key = Path(datum["filename"]).suffix.replace(".", "")
                if original_file_key in parser.allowed_types:
                    parsed_file = parser.parse(datum, logger)
                    collection_key = parsed_file.file_extension.replace(".", "")
                    parsed_file_collection[collection_key] = parsed_file

            parsed_file_collections.append(
                ParsedFileCollection(**parsed_file_collection)
            )

        return parsed_file_collections

    def _add_original_file_data(self, parsed_file_collection_data: dict, datum: dict):
        original_file_extension = Path(datum["filename"]).suffix.replace(".", "")
        original_file_data = {**datum, "file_extension": original_file_extension}
        parsed_file_collection_data["original"] = ParsedFile(**original_file_data)

        return parsed_file_collection_data
