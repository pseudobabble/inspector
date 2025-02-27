import unittest
from hashlib import md5
from unittest.mock import MagicMock, Mock, patch

from document_processing.builder import DocumentBuilder, DocumentExistsException
from document_processing.models import Document, MLDocument, RawDocument


class TestDocumentBuilder(unittest.TestCase):
    def test_build(self):
        mock_repository_get_by_hash = Mock(return_value=None)
        mock_repository_save = Mock()
        mock_repository = Mock(
            get_by_hash=mock_repository_get_by_hash, save=mock_repository_save
        )

        raw_document = RawDocument(filename="test.py", content="abc123")
        content_hash = str(md5(raw_document.content.encode("utf-8")))

        builder = DocumentBuilder(document_repository=mock_repository)
        document = builder.build(raw_document)

        mock_repository_get_by_hash.assert_called_with(content_hash)
        mock_repository_save.assert_called()
        assert document.filename == raw_document.filename
        assert document.raw_content == raw_document.content
        assert document.content_hash == content_hash

    def test_build_expect_document_exists_exception(self):
        return_document = Document(id=1, filename="test_file.py", raw_content="abc123")

        mock_repository_get_by_hash = Mock(return_value=return_document)
        mock_repository_save = Mock()
        mock_repository = Mock(
            get_by_hash=mock_repository_get_by_hash, save=mock_repository_save
        )

        raw_document = RawDocument(filename="test.py", content="abc123")
        content_hash = str(md5(raw_document.content.encode("utf-8")))

        builder = DocumentBuilder(document_repository=mock_repository)

        with self.assertRaises(DocumentExistsException):
            builder.build(raw_document)

        mock_repository_get_by_hash.assert_called_with(content_hash)

    def test_update_documents_with_ml_document(self):
        return_document = Document(id=1, filename="test_file.py", raw_content="abc123")

        mock_repository_get_by_ids = Mock(return_value=[return_document])
        mock_repository_save_multiple = Mock()
        mock_repository = Mock(
            get_by_ids=mock_repository_get_by_ids,
            save_multiple=mock_repository_save_multiple,
        )

        ml_documents = [
            {
                "id": "ab28128e-4a33-40f1-ae61-b3658cb461dc",
                "content": "abc123",
                "content_type": "text",
                "meta": {"document_id": 1, "filename": "test.py", "_split_id": 0},
            },
            {
                "id": "ab28128e-4a33-40f1-ae61-b3658cb461dc",
                "content": "abc123",
                "content_type": "text",
                "meta": {"document_id": 2, "filename": "test.py", "_split_id": 0},
            },
        ]

        builder = DocumentBuilder(document_repository=mock_repository)
        builder.update_documents_with_ml_documents(ml_documents)

        mock_repository_get_by_ids.assert_called_with([1, 2])
        mock_repository.save_multiple.assert_called_with([return_document])
        ml_document_created = MLDocument(
            document_id=1,
            content="abc123",
            content_type="text",
            ml_id="ab28128e-4a33-40f1-ae61-b3658cb461dc",
            meta={"meta": {"document_id": 2, "filename": "test.py", "_split_id": 0}},
            score=None,
            embedding=None,
            id_hash_keys=None,
        )

        assert return_document.ml_documents[0].content == ml_document_created.content
        assert (
            return_document.ml_documents[0].document_id
            == ml_document_created.document_id
        )
        assert (
            return_document.ml_documents[0].content_type
            == ml_document_created.content_type
        )


if __name__ == "__main__":
    unittest.main()
