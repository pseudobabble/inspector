import unittest
from unittest.mock import MagicMock, Mock, patch

from document_processing.models import Document, RawDocument
from document_processing.resources import Documents

class TestDocuments(unittest.TestCase):

    @patch('document_processing.resources.flask')
    def test_get_all(self, mock_flask):
        mock_flask.request.args = {}
        return_document = Document(
            id=1,
            filename='test_file.py',
            raw_content='abc123'
        )
        mock_repository_get_all = Mock(return_value=[return_document])
        mock_repository = Mock(get_all=mock_repository_get_all)

        mock_schema_dump = Mock(return_value='DUMP')
        mock_schema = Mock(dump=mock_schema_dump)

        documents_resource = Documents(
            document_schema=mock_schema,
            document_repository=mock_repository
        )

        result = documents_resource.get()

        assert result == 'DUMP'
        mock_repository_get_all.assert_called()
        mock_schema_dump.assert_called_with([return_document], many=False)

    @patch('document_processing.resources.flask')
    def test_get_by_ids(self, mock_flask):
        mock_flask.request.get_json.return_value = {'ids': [1]}

        return_document = Document(
            id=1,
            filename='test_file.py',
            raw_content='abc123'
        )
        mock_repository_get_by_ids = Mock(return_value=[return_document])
        mock_repository = Mock(get_by_ids=mock_repository_get_by_ids)

        mock_schema_dump = Mock(return_value='DUMP')
        mock_schema = Mock(dump=mock_schema_dump)

        documents_resource = Documents(
            document_schema=mock_schema,
            document_repository=mock_repository
        )

        result = documents_resource.get_by_ids()

        assert result == ['DUMP']
        mock_repository_get_by_ids.assert_called_with([1])
        mock_schema_dump.assert_called_with(return_document)

    @patch('document_processing.resources.flask')
    def test_post(self, mock_flask):
        mock_flask.request.get_json.return_value = {'filename': 'test.py', 'content': 'abc123'}

        return_document = Document(
            id=1,
            filename='test_file.py',
            raw_content='abc123'
        )
        mock_builder_build = Mock(return_value=return_document)
        mock_builder = Mock(build=mock_builder_build)

        mock_schema_dump = Mock(return_value='DUMP')
        mock_schema = Mock(dump=mock_schema_dump)

        documents_resource = Documents(
            document_schema=mock_schema,
            document_builder=mock_builder
        )

        result = documents_resource.post()

        assert result == 'DUMP'
        mock_builder_build.assert_called_with(RawDocument(filename='test.py', content='abc123'))
        mock_schema_dump.assert_called_with(return_document)

    @patch('document_processing.resources.flask')
    def test_upload(self, mock_flask):
        mock_flask.request.method = 'POST'

        mock_file_read = Mock(return_value='abc123')
        mock_flask_file = Mock(filename='test.py', read=mock_file_read)
        mock_getlist = Mock(return_value=[mock_flask_file])
        mock_flask.request.files = Mock(getlist=mock_getlist)

        return_document = Document(
            id=1,
            filename='test_file.py',
            raw_content='abc123'
        )
        mock_builder_build = Mock(return_value=return_document)
        mock_builder = Mock(build=mock_builder_build)

        mock_schema_dump = Mock(return_value='DUMP')
        mock_schema = Mock(dump=mock_schema_dump)

        documents_resource = Documents(
            document_schema=mock_schema,
            document_builder=mock_builder
        )

        result = documents_resource.upload()

        assert result == ['DUMP']
        mock_builder_build.assert_called_with(RawDocument(filename='test.py', content='abc123'))
        mock_schema_dump.assert_called_with(return_document)

    @patch('document_processing.resources.flask')
    def test_patch(self, mock_flask):
        response_json = [{
            'id': 'ab28128e-4a33-40f1-ae61-b3658cb461dc',
            'content': 'abc123',
            'content_type': 'text',
            'meta': {
                'document_id': 1,
                'filename': 'test.py',
                '_split_id': 0
            }
        }]
        mock_flask.request.get_json.return_value = response_json

        return_document = Document(
            id=1,
            filename='test_file.py',
            raw_content='abc123'
        )
        mock_builder_update_documents_with_ml_documents = Mock(return_value=[return_document])
        mock_builder = Mock(update_documents_with_ml_documents=mock_builder_update_documents_with_ml_documents)

        documents_resource = Documents(
            document_builder=mock_builder
        )

        result = documents_resource.patch()

        assert result == {'success': 200}
        mock_builder_update_documents_with_ml_documents.assert_called_with(response_json)


if __name__ == '__main__':
    unittest.main()
