import unittest

from adaptors.rest.schemata import (
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
