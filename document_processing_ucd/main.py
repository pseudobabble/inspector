"""This module is the top level for document processing pipeline code"""
import nltk
from dagster import job, repository

from ops.documents import (
    get_file_keys,
    get_file_from_document_store,
    put_file_to_document_store,
    convert_with_tika,
    get_raw_documents,
    preprocess_raw_documents,
    retrieve_candidates,
    save_ml_documents_to_document_store,
    semantic_refine_candidates,
)
from graphs.documents import convert_files_to_text
from resources.components import preprocessor, reader, retriever
from resources.files import blob_client, file_parser
from resources.persistence import sql_document_store
from resources.webapp import answer_client, raw_documents_repository
from resources.convert import tika_client

nltk.download("punkt")





@job(
    resource_defs={
        "document_store": sql_document_store,
        "raw_documents_repository": raw_documents_repository,
        "retriever": retriever,
        "reader": reader,
        "answer_client": answer_client,
    }
)
def answer_query():
    candidates = retrieve_candidates()
    semantic_refine_candidates(candidates)


@repository
def document_processing():
    return [
        answer_query,
    ]
