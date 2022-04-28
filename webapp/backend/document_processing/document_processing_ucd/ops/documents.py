from typing import List
from hashlib import md5

from dagster import op


@op(
    config_schema={"document_ids": Array(int)},
    required_resource_keys={"document_store", "raw_documents_repository"}
)
def get_raw_documents(context):
    logger = context.log

    document_ids = context.op_config['document_ids']

    document_store = context.resources.document_store
    raw_documents_repository = context.resources.raw_documents_repository

    logger.info("Processing documents for ids %s", document_ids)

    raw_documents = raw_documents_repository.get_by_ids(document_ids)
    logger.info(
        "Found %s documents to process: %s",
        len(raw_documents),
        [d['document_id'] for d in raw_documents]
    )

    return raw_documents


@op(
    required_resource_keys={"raw_documents_repository"}
)
def update_documents(ml_documents: List[MLDocument]):
    response = raw_documents_repository.update_documents(ml_documents)
    logger.info("Update response: %s", response.status_code)

    return preprocessed_docs


@op(
    required_resource_keys={"document_store", "preprocessor"}
)
def preprocess_raw_documents(context, raw_documents: List[Dict]):
    logger = context.log

    document_store = context.resources.document_store
    preprocessor = context.resources.preprocessor

    preprocessed_docs = preprocessor.process(raw_documents)

    return preprocessed_docs


@op(
    required_resource_keys={"document_store"}
)
def save_ml_documents(context, ml_documents: List[MLDocument]):
    document_store = context.resources.document_store
    for doc in ml_documents:
        doc['id'] = md5(doc['content'].encode('utf-8')).hexdigest()

    document_store.write_documents(ml_documents)
    logger.info(
        "Updating documents with %s MLDocuments",
        len(ml_documents)
    )

    return ml_documents


@op(
    config_schema={
        "query": str,
        "top_k": int
    },
    required_resource_keys={"document_store", "reader"}
)
def refine_candidates(context, candidate_documents: List[MLDocument]):
    logger = context.log

    query = context.op_config['query']
    top_k = context.op_config['top_k']

    document_store = context.resources.document_store
    reader = context.resources.reader

    query_results = reader.predict(
        query=query,
        documents=candidate_documents,
        top_k=top_k
    )

    return query_results


@op(
    config_schema={
        "query": str,
        "top_k": int
    },
    required_resource_keys={"document_store", "retriever"}
)
def retrieve_candidates(context, candidate_documents: List[MLDocument]):
    logger = context.log

    query = context.op_config['query']
    top_k = context.op_config['top_k']

    document_store = context.resources.document_store
    retriever = context.resources.retriever

    candidates = retriever.retrieve(
        query=query,
        documents=document_store.get_all_documents(),
        top_k=top_k
    )

    candidates = retriever(document_store)

    return candidates
