import os
from hashlib import md5
from pathlib import Path
from typing import List

import torch
from dagster import Array, op, DynamicOut, DynamicOutput
from dagster_shell import create_shell_command_op
from haystack.schema import Document
from sentence_transformers import SentenceTransformer, util

from adaptors.rest.webhook import Answer

@op(
    config_schema={"keys": Array(str)},
    out=DynamicOut(str)
)
def get_file_keys(context):
    config = context.op_config
    keys = config['keys']

    for key in keys:
        yield DynamicOutput(
            value=key,
            mapping_key=key
        )

@op(
    required_resource_keys={"blob_client"},
)
def get_file_from_document_store(context, file_key: str):
    logger = context.log

    blob_client = context.blob_client

    logger.info('Getting %s from document store', f"{file_key}/original")
    file_content = blob_client.get(file_key)

    return file_content

@op(
    required_resource_keys={"blob_client"},
)
def put_file_to_document_store(context, file_key, file_content):
    logger = context.log

    blob_client = context.blob_client

    logger.info('Putting %s to document store', file_key)
    response = blob_client.put(f"{file_key}/text", file_put_file_to_document_content)

    return response

@op(
    required_resource_keys={"tika_client"},
)
def convert_with_tika(context, file_content: bytes):
    logger = context.log

    tika_client = context.resources.tika_client

    logger.info('Converting file to text with tika')

    document_extension = Path(raw_document['filename']).suffix
    if not document_extension in tika_client.allowed_types:
        raise ValueError(
            'Document type %s not allowed. Allowed types are %s',
            document_extension,
            ', '.join(list(tika_client.allowed_types))
        )
    document_text = tika_client.convert_text(file_content, document_extension)

    return document_text




@op(
    config_schema={"document_ids": Array(int)},
    required_resource_keys={"raw_documents_repository"},
)
def get_raw_documents(context):
    logger = context.log

    document_ids = context.op_config["document_ids"]

    raw_documents_repository = context.resources.raw_documents_repository

    logger.info("Processing documents for ids %s", document_ids)
    raw_documents = raw_documents_repository.get_by_ids(document_ids)
    logger.info(raw_documents)
    logger.info(
        "Found %s documents to process: %s",
        len(raw_documents),
        [d["document_id"] for d in raw_documents],
    )

    for d in raw_documents:
        d["meta"] = {"document_id": d["document_id"]}

    return raw_documents


@op(required_resource_keys={"raw_documents_repository"})
def update_documents(context, ml_documents: List[Document]):
    logger = context.log

    raw_documents_repository = context.resources.raw_documents_repository

    logger.info(
        "Updating domain with %s MLDocuments: %s", len(ml_documents), ml_documents
    )
    response = raw_documents_repository.update_documents(ml_documents)
    logger.info("Update response: %s", response.status_code)

    return ml_documents


@op(required_resource_keys={"document_store", "preprocessor"})
def preprocess_raw_documents(context, raw_text_documents: List[dict]):
    logger = context.log

    preprocessor = context.resources.preprocessor

    for document in raw_text_documents:
        document["content"] = document["content"].decode("utf-8")

    preprocessed_docs = preprocessor.process(raw_text_documents)
    logger.info(
        "Preprocessed %s raw_documents into %s preprocessed docs",
        len(raw_text_documents),
        len(preprocessed_docs),
    )

    return preprocessed_docs


@op(required_resource_keys={"document_store"})
def save_ml_documents_to_document_store(
    context,
    preprocessed_documents: List[Document],
):
    logger = context.log

    document_store = context.resources.document_store

    for doc in preprocessed_documents:
        doc.id = md5(doc.content.encode("utf-8")).hexdigest()

    document_store.write_documents(preprocessed_documents)
    logger.info(
        "Updating documents with %s MLDocuments: %s",
        len(preprocessed_documents),
        [d.id for d in preprocessed_documents],
    )

    return preprocessed_documents


@op(config_schema={"query": str, "top_k": int}, required_resource_keys={"reader"})
def refine_candidates(context, candidate_documents: List[Document]):
    logger = context.log

    query = context.op_config["query"]
    top_k = context.op_config["top_k"]
    logger.info("Refining candidates for query '%s'")

    reader = context.resources.reader

    query_results = reader.predict(
        query=query, documents=candidate_documents, top_k=top_k
    )
    logger.info("Refined query results: %s", query_results)

    return query_results


@op(
    config_schema={"query": str, "top_k": int},
    required_resource_keys={"document_store", "retriever"},
)
def retrieve_candidates(context):
    logger = context.log

    query = context.op_config["query"]
    top_k = context.op_config["top_k"]
    logger.info("Retrieving %s candidates for query '%s'", top_k, query)

    retriever = context.resources.retriever

    candidates = retriever.retrieve(query=query, top_k=top_k)
    logger.info(
        "Found %s candidates for query '%s': %s", len(candidates), query, candidates
    )

    return candidates


@op(
    config_schema={"query": str, "top_k": int}, required_resource_keys={"answer_client"}
)
def semantic_refine_candidates(context, candidate_documents: List[Document]):
    logger = context.log

    query = context.op_config["query"]
    top_k = context.op_config["top_k"]
    logger.info("Refining candidates for query '%s'", query)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    corpus = [d.content for d in candidate_documents]
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    query_results = torch.topk(cos_scores, k=top_k)

    result_log, answers = "", []
    for score, idx, *rest in zip(*query_results):
        snippet = corpus[idx]
        result_log += "\n\n{}, (Score: {:.4f})\n\n".format(snippet, score)
        result_log += "=" * 20 + "\n" + " DEBUG OUT"
        result_log += (
            "==>  " + ", ".join([repr(item) for item in [score, idx, *rest]]) + "\n"
        )
        result_log += "=" * 20 + "\n"

        answers += [Answer(index=repr(idx), score=repr(score), snippet=repr(snippet))]
    logger.info("Refined query results: %s", result_log)

    client = context.resources.answer_client
    client.post(answers)

    return None
