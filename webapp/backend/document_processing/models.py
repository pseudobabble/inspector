from dataclasses import dataclass
from typing import Union, Literal, Dict, Optional, Any, List
import uuid
import pickle

import sqlalchemy.types as types
from sqlalchemy import Column, Integer, String, Float, ForeignKey, TypeDecorator
from sqlalchemy.orm import composite, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils import UUIDType, JSONType
import pandas as pd
import numpy as np

from infrastructure import repository


class Document(repository.Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    filename = Column(String(length=50), unique=True)
    raw_content = Column(String)
    content_hash = Column(String)
    ml_documents = relationship("MLDocument")


class NumpyArray(TypeDecorator):

    impl = types.PickleType

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = value.dumps()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = pickle.loads(value)
        return value


class MLDocument(repository.Base):
    __tablename__ = "ml_documents"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4) # originates in the pipeline
    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("Document", back_populates="ml_documents")
    content = Column(String) # could be df?
    content_type = Column(String)
    meta = Column(JSONType)
    score = Column(Float, nullable=True)
    embedding = Column(NumpyArray, nullable=True)
    id_hash_keys = Column(ARRAY(String), nullable=True)
