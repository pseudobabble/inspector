"""This module is the top level for document processing pipeline code"""
from typing import List
from dataclasses import dataclass, asdict
from dagster import repository, job

from document_processing.resources.webapp import raw_documents_repository
from document_processing.resources.persistence import sql_document_store
from document_processing.resources.components import preprocessor, retriever, reader

from document_processing.resources.ops.documents import get_raw_documents \
    preprocess_raw_documents, update_documents, save_ml_documents, \
    retrieve_candidates, refine_candidates


nltk.download('punkt')



@job(
    resource_defs={
        'document_store': sql_document_store,
        "raw_documents_repository": raw_documents_repository,
        "preprocessor": preprocessor,
)
def preprocess_documents():
    raw_documents = get_raw_documents()
    preprocessed_ml_documents = preprocess_raw_documents(raw_documents)
    ml_documents = save_ml_documents(preprocessed_ml_documents)
    ml_documents = update_documents(ml_documents)


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
