from typing import List
from hashlib import md5

from haystack.nodes import PreProcessor, FARMReader, TfidfRetriever
from dagster import op


nltk.download('punkt')

@op(
    required_resource_keys={"document_store"}
)
def preprocessor(context, raw_documents: List[Dict]):
    logger = context.log
    op_config = context.op_config
    document_store = context.resources.document_store

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

    documents = document_store.get_all_documents()

    # TODO: extract retriever and config to configurable resource
    retriever = TfidfRetriever(document_store=document_store)
    candidates = retriever.retrieve(
        query=op_config['query'],
        documents=documents,
        top_k=10
    )

    return candidates
