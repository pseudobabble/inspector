from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import LargeBinary
from sqlalchemy_utils import UUIDType, JSONType

from infrastructure import repository


class Document(repository.Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String(length=50), unique=True)
    raw_content = Column(LargeBinary)
    content_hash = Column(String)
    ml_documents = relationship("MLDocument")


class MLDocument(repository.Base):
    __tablename__ = "ml_documents"

    id = Column(Integer, primary_key=True)
    document_store_id = Column(String)
    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document", back_populates="ml_documents")
    # run id


class Query(repository.Base):

    __tablename__ = "queries"

    id = Column(UUIDType, primary_key=True, default=uuid4())
    run_id = Column(UUIDType(binary=False))
    answers = Column(JSONType)
