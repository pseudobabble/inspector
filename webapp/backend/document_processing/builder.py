from hashlib import md5
from typing import List

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

    def update_documents_with_ml_documents(self, ml_documents: List[dict]):
        ml_document_ids = [d['meta']['document_id'] for d in ml_documents]

        documents = self.document_repository.get_by_ids(ml_document_ids)
        documents_by_id = {d.id: d for d in documents}

        updated_documents = []
        for ml_document_data in ml_documents:
            ml_document_id = ml_document_data['meta']['document_id']
            # TODO: Assuming they have the same id..
            document = documents_by_id.get(ml_document_id)
            if document:
                ml_document = MLDocument(
                    document_id=document.id,
                    content=ml_document_data['content'],
                    content_type=ml_document_data['content_type'],
                    ml_id=ml_document_data['id'],
                    meta=ml_document_data['meta'],
                    score=ml_document_data.get('score', None),
                    embedding=ml_document_data.get('embedding', None),
                    id_hash_keys=ml_document_data.get('id_hash_keys', None),
                )
                document.ml_documents.append(ml_document)
                updated_documents.append(document)

        self.document_repository.save_multiple(updated_documents)
