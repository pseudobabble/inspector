"""This module is the top level for document processing pipeline code"""
from typing import List
from dataclasses import dataclass, asdict

from dagster import repository, job
import nltk

from resources.webapp import raw_documents_repository
from resources.files import file_parser, blob_client
from resources.persistence import sql_document_store
from resources.components import preprocessor, retriever, reader

from ops.documents import get_raw_documents, \
    preprocess_raw_documents, update_documents, save_ml_documents, \
    retrieve_candidates, refine_candidates, store_files


nltk.download('punkt')


@job(
    resource_defs={
        'document_store': sql_document_store,
        "raw_documents_repository": raw_documents_repository,
        "preprocessor": preprocessor,
        "file_parser": file_parser,
        "blob_client": blob_client
    }
)
def preprocess_documents():
    raw_documents = get_raw_documents()
    store_files(raw_documents)
    preprocessed_ml_documents = preprocess_raw_documents(raw_documents)
    ml_documents = save_ml_documents(preprocessed_ml_documents)
    update_documents(ml_documents)


@job(
    resource_defs={
        'document_store': sql_document_store,
        "raw_documents_repository": raw_documents_repository,
        "retriever": retriever,
        "reader": reader
    }
)
def answer_query():
    candidates = retrieve_candidates()
    answers = refine_candidates(candidates)

@repository
def document_processing():
    return [
        preprocess_documents,
        answer_query,
    ]
