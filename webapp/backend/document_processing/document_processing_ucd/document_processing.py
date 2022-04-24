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
from dagster import repository, job, op, graph, resource, In, Array

from schemata import PipelineToMLDocument
from document_processing.resources.webapp import raw_documents_repository
from document_processing.resources.persistence import sql_document_store

nltk.download('punkt')


@op(
    required_resource_keys={"document_store"}
)
def preprocess_docs(context, raw_documents: List[Dict]):

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
        'document_store': sql_document_store,
        "raw_documents_repository": raw_documents_repository
    }
)
def preprocess_documents():
    raw_documents = get_raw_documents()
    preprocess_docs()


@job(
    resource_defs={
        'document_store': sql_document_store,
        "raw_documents_repository": raw_documents_repository
    }
)
def answer_query():
    candidates = retriever()
    answers = reader(candidates)

@repository
def document_processing():
    return [
        preprocess_documents,
        answer_query,
    ]
