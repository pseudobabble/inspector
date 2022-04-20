"""This module is the top level for document processing pipeline code"""
from typing import List
from dataclasses import dataclass, asdict
import json
import logging
from uuid import uuid4
from hashlib import md5

import requests
import nltk
from haystack.document_stores import SQLDocumentStore
from haystack.nodes import TextConverter, PDFToTextConverter, \
    DocxToTextConverter, PreProcessor, TfidfRetriever
from haystack.schema import Document as MLDocument
from dagster import job, op, graph, resource, In, Array

from schemata import PipelineToMLDocument

nltk.download('punkt')


class RawDocumentsRepository:

    def __init__(
            self,
            dagster_init_context,
            client = requests,
            pipeline_to_document_schema = PipelineToMLDocument()
    ):
        self.url = dagster_init_context.resource_config.get('url')
        self.client = client
        self.pipeline_to_document_schema = pipeline_to_document_schema

    def get_by_ids(self, document_ids: List[int]):
        documents_response = self.client.get(
            self.url,
            params={"ids": json.dumps(document_ids)}
        )

        raw_documents = [d for d in documents_response.json()]

        return raw_documents

    def update_documents(self, ml_documents: List[MLDocument]):
        # TODO: do we want to keep sending the whole document, or just ids?
        update_response = self.client.patch(
            self.url,
            json=self.pipeline_to_document_schema.dump(ml_documents, many=True)
        )

        return update_response

@resource(config_schema={"url": str})
def raw_documents_repository(init_context):
    return RawDocumentsRepository(init_context)

@resource(config_schema={"url": str})
def document_store(init_context):
    return SQLDocumentStore(
        url=init_context.resource_config.get('url')
    )

@op(
    config_schema={"document_ids": Array(int)},
    required_resource_keys={"document_store", "raw_documents_repository"}
)
def preprocess_docs(context):
    logger = context.log
    op_config = context.op_config
    document_store = context.resources.document_store
    raw_documents_repository = context.resources.raw_documents_repository

    document_ids = op_config['document_ids']
    logger.info("Processing documents for ids %s", document_ids)

    raw_documents = raw_documents_repository.get_by_ids(document_ids)
    logger.info(
        "Found %s documents to process: %s",
        len(raw_documents),
        [d['document_id'] for d in raw_documents]
    )

    # TODO: extract the preprocessor to a configurable resource
    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=100,
        split_respect_sentence_boundary=True
    )
    preprocessed_docs = preprocessor.process(raw_documents)

    # TODO: Sort this out
    for doc in preprocessed_docs:
        doc['id'] = md5(doc['content'].encode('utf-8')).hexdigest()

    document_store.write_documents(preprocessed_docs)
    logger.info(
        "Updating documents with %s MLDocuments",
        len(preprocessed_docs)
    )

    response = raw_documents_repository.update_documents(preprocessed_docs)
    logger.info("Update response: %s", response.status_code)

    return preprocessed_docs

@op(
    config_schema={"query": str},
    required_resource_keys={"document_store", "raw_documents_repository"}
)
def reader(context, candidate_documents: List[MLDocument]):
    logger = context.log
    op_config = context.op_config
    document_store = context.resources.document_store
    raw_documents_repository = context.resources.raw_documents_repository

    # TODO: extract reader and config to configurable resource
    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
    query_results = reader.predict(
        query=op_config['query'],
        documents=candidate_documents,
        top_k=10
    )

    return query_results

@op(
    config_schema={"query": str},
    required_resource_keys={"document_store", "raw_documents_repository"}
)
def retriever(context):
    logger = context.log
    op_config = context.op_config
    document_store = context.resources.document_store
    raw_documents_repository = context.resources.raw_documents_repository

    documents = document_store.get_all_documents()

    # TODO: extract retriever and config to configurable resource
    retriever = TfidfRetriever(document_store=document_store)
    candidates = retriever.retrieve(
        query=op_config['query'],
        documents=documents,
        top_k=10
    )

    return candidates

@job(
    resource_defs={
        'document_store': document_store,
        "raw_documents_repository": raw_documents_repository
    }
)
def preprocess_documents():
    preprocess_docs()


@job(
    resource_defs={
        'document_store': document_store,
        "raw_documents_repository": raw_documents_repository
    }
)
def answer_query():
    candidates = retriever()
    answers = reader(candidates)
