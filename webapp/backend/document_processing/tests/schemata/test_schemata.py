import unittest
from unittest.mock import MagicMock, Mock, patch

from document_processing.schemata import (
    Document,
    DocumentToPipeline,
    MLDocument,
    PipelineToMLDocument,
    RawDocument,
)


class TestDocumentBuilder(unittest.TestCase):
    def test_raw_document(self):
        input_json = {"filename": "test.py", "content": "abc123"}

        raw_document_schema = RawDocument()
        loaded_raw_document = raw_document_schema.load(input_json)

        assert loaded_raw_document == input_json


if __name__ == "__main__":
    unittest.main()
