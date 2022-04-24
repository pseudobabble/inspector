from hashlib import md5
from typing import List

from .models import Document, MLDocument
from .repository import DocumentRepository


class DocumentExistsException(Exception):
    pass


class DocumentBuilder:

    def __init__(
            self,
            document_repository: DocumentRepository = DocumentRepository()
    ) -> None:
        self.document_repository = document_repository

    def build(self, document: dict) -> None:
        content_hash = md5(document['content']).hexdigest()
        existing_document = self.document_repository.get_by_hash(content_hash)

        if existing_document:
            raise DocumentExistsException(
                f"Document with content hash {str(content_hash)} already exists."
            )

        document = Document(
            filename=document['filename'], raw_content=document['content'], content_hash=str(content_hash)
        )
        self.document_repository.save(document)

        return document

    def update_documents_with_ml_documents(self, ml_documents: List[dict]):
        ml_document_ids = [d['meta']['document_id'] for d in ml_documents] # TODO: deduplicate them

        documents = self.document_repository.get_by_ids(ml_document_ids)
        documents_by_id = {d.id: d for d in documents}

        updated_documents = []
        for ml_document_data in ml_documents: # TODO: maybe invert the iteration for performance
            document_id = ml_document_data['meta']['document_id']
            document = documents_by_id.get(document_id)
            if document:
                ml_document = MLDocument(
                    document_store_id = ml_document_data['id'],
                    document_id = document.id,
                    document = document
                )
                document.ml_documents.append(ml_document)
                updated_documents.append(document)

        self.document_repository.save_multiple(updated_documents)

        return updated_documents
