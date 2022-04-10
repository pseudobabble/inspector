"""This module is the top level for document processing pipeline code"""
from typing import List
from dataclasses import dataclass, asdict
import json
import logging

import requests
from haystack.document_stores import SQLDocumentStore
from haystack.nodes import TextConverter, PDFToTextConverter, DocxToTextConverter, PreProcessor
from haystack.schema import Document as MLDocument
from dagster import job, op, graph, resource, In, Array


@dataclass(frozen=True, eq=True, repr=True)
class RawDocument:
    filename: str
    content: str


class RawDocumentsRepository:

    def __init__(
            self,
            dagster_init_context,
            client = requests,
            serializer = json
    ):
        self.init_context = dagster_init_context
        self.url = dagster_init_context.resource_config.get('url')
        self.client = client
        self.serializer = serializer

    def get_by_ids(self, document_ids: List[int]):
        documents_response = self.client.get(
            self.url,
            data=self.serializer.dumps({"ids": document_ids})
        )
        logging.info(documents_response.json())

        raw_documents = [
            RawDocument(filename=d.filename, content=d.content)
            for d in documents_response.json()
        ]

        return raw_documents

    def update_documents(self, ml_documents: List[MLDocument]):
        ml_document_dicts = [ml_document.to_dict() for ml_document in ml_documents]
        update_response = self.client.patch(self.url, data=self.serializer.dumps(ml_document_dicts))
        pass

@resource(config_schema={"url": str})
def raw_documents_repository(init_context):
    return RawDocumentsRepository(init_context)

@resource(config_schema={"url": str})
def document_store(init_context):
    #url='postgresql://webapp_postgres_user:webapp_postgres_password@webapp-postgres:5432/webapp_postgres_db',
    return SQLDocumentStore(
        url=init_context.resource_config.get('url')
    )

# TODO: spec this up to be generalized - take a file converter, params, etc
@op(
    config_schema={"document_ids": Array(int)},
    required_resource_keys={"document_store", "raw_documents_repository"}
)
def preprocess_docs(context):
    op_config = context.op_config
    document_store = context.resources.document_store
    raw_documents_repository = context.resources.raw_documents_repository

    raw_documents = raw_documents_repository.get_by_ids(op_config['document_ids'])

    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=100,
        split_respect_sentence_boundary=True,
    )
    preprocessed_docs = preprocessor.process([asdict(raw_document) for raw_document in raw_documents])
    document_store.write_documents(preprocessed_docs)
    raw_documents_repository.update_documents(preprocessed_docs)

    return preprocessed_docs



@job(
    resource_defs={
        'document_store': document_store,
        "raw_documents_repository": raw_documents_repository
    }
)
def preprocess_documents():
    preprocess_docs()
