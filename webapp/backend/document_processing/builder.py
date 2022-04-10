from hashlib import md5

from infrastructure.dagster_client import DagsterClient
from .models import Document, RawDocument, MLDocument
from .repository import DocumentRepository


class DocumentExistsException(Exception):
    pass


class DocumentBuilder:

    def __init__(
            self,
            document_repository: DocumentRepository = DocumentRepository()
    ) -> None:
        self.document_repository = document_repository

    def build(self, document: RawDocument) -> None:
        content_hash = str(md5(document.content.encode('utf-8')))
        existing_document = self.document_repository.get_by_hash(content_hash)

        if existing_document:
            raise DocumentExistsException(
                f"Document with content hash {str(content_hash)} already exists."
            )

        document = Document(
            filename=document.filename, raw_content=document.content, content_hash=content_hash
        )
        self.document_repository.save(document)

        return document

    def update_documents_with_ml_document(self, ml_documents: dict):
        ml_document_ids = [d['id'] for d in ml_documents.items()]

        documents = self.document_repository.get_by_ids(ml_document_ids)
        documents_by_id = {d.id: d for d in documents}

        for ml_document_data in ml_documents.items():
            ml_document_id = ml_document_data['id']
            document = documents_by_id.get(ml_document_id)
            if document:
                del ml_document_data['id']
                ml_document_data['document_id'] = document.id
                ml_document = MLDocument.from_dict(ml_document_data)
                document.ml_documents.append(ml_document)

        self.document_repository.save_multiple()
