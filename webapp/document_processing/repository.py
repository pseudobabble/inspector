from typing import List
from uuid import uuid4

from infrastructure.repository.sqlalchemy_adaptor import SqlAlchemyAdaptor

from .models import Document, Query

DocumentList = List[Document]


class UnexpectedEntityException(Exception):
    ...

class QueryRepository(SqlAlchemyAdaptor):

    entity = Query

    def get_by_run_id(self, run_id: uuid4):
        return (
            self.session.query(self.entity)
            .filter(self.entity.run_id == run_id)
            .first()
        )

class DocumentRepository(SqlAlchemyAdaptor):
    """
    The DocumentRepository represents a collection of Documents.
    It is the means by which Documents and their associated Revisions are
    retrieved from and posted to persistent storage.
    """

    entity = Document

    def get_all(self) -> DocumentList:
        """
        Get all Documents in storage
        :return: DocumentList
        """
        return self.session.query(self.entity).all()

    def get_by_hash(self, content_hash: str) -> Document:
        return (
            self.session.query(self.entity)
            .filter(self.entity.content_hash == content_hash)
            .first()
        )

    def get_by_ids(self, document_ids: List[int]):
        return (
            self.session.query(self.entity)
            .filter(self.entity.id.in_(document_ids))
            .all()
        )

    def save_multiple(self, documents: List[Document]):
        for document in documents:
            if not isinstance(document, self.entity):
                raise UnexpectedEntityException(
                    f"Expected {self.entity}, found {type(document)}"
                )

        self.session.add_all(documents)
        self.session.commit()
