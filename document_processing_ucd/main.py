"""This module is the top level for document processing pipeline code"""
import nltk
from dagster import job, repository

from ops.documents import (docs_to_text, get_raw_documents,
                           preprocess_raw_documents, refine_candidates,
                           retrieve_candidates,
                           save_ml_documents_to_document_store,
                           store_converted_files, update_documents,
                           write_input_files, semantic_refine_candidates)
from resources.components import preprocessor, reader, retriever
from resources.files import blob_client, file_parser
from resources.persistence import sql_document_store
from resources.webapp import raw_documents_repository

nltk.download("punkt")


@job(
    resource_defs={
        "document_store": sql_document_store,
        "raw_documents_repository": raw_documents_repository,
        "preprocessor": preprocessor,
        "file_parser": file_parser,
        "blob_client": blob_client,
    }
)
def preprocess_documents():
    raw_documents = get_raw_documents()
    raw_documents = write_input_files(raw_documents)
    raw_documents = docs_to_text(raw_documents)
    raw_text_documents = store_converted_files(raw_documents)
    preprocessed_ml_documents = preprocess_raw_documents(raw_text_documents)
    preprocessed_ml_documents = save_ml_documents_to_document_store(
        preprocessed_ml_documents
    )
    update_documents(preprocessed_ml_documents)


@job(
    resource_defs={
        "document_store": sql_document_store,
        "raw_documents_repository": raw_documents_repository,
        "retriever": retriever,
        "reader": reader,
    }
)
def answer_query():
    candidates = retrieve_candidates()
    semantic_refine_candidates(candidates)


@repository
def document_processing():
    return [
        preprocess_documents,
        answer_query,
    ]
