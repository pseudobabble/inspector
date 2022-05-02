from typing import List
from hashlib import md5
import os
from pathlib import Path
import time
import subprocess
import shlex

from dagster import op, Array
from dagster_shell import create_shell_command_op

from schemata import MLDocument


# op which just runs a shell command
convert_input_doc_files = create_shell_command_op(
    '/usr/bin/soffice --headless --convert-to txt:Text --outdir ./tmp/txt/ ./tmp/docs_in/*.doc ./tmp/docs_in/*.docx',
    name='convert_input_doc_files'
)

@op
def docs_to_text(context, raw_documents: List[dict]):
    logger = context.log

    paths = os.listdir('./tmp/docs_in')
    logger.info("Converting docs to text: %s", paths)

    result = os.system(
        '/usr/bin/soffice "-env:UserInstallation=file:///tmp/LibreOffice_Conversion_root" --headless --convert-to txt:Text --outdir ./tmp/txt/ ./tmp/docs_in/*.doc ./tmp/docs_in/*.docx'
    )
    logger.info("Converted files: %s", os.listdir('./tmp/txt'))

    return raw_documents

@op(
    required_resource_keys={"blob_client"}
)
def write_input_files(context, raw_documents: List[dict]):
    logger = context.log
    logger.info("Received %s raw_documents", len(raw_documents))

    blob_client = context.resources.blob_client

    logger.info("Putting %s original files to blob store", len(raw_documents))
    logger.info("Writing %s files to filesystem for conversion", len(raw_documents))
    for d in raw_documents:
        # store original content
        filename_path = Path(d['filename'])
        file_extension = filename_path.suffix
        filename_stem = filename_path.stem
        key = f"{filename_stem}/original{file_extension}"
        blob_client.put(key, d['content'])

        # write to filesystem for conversion
        os.makedirs('./tmp/docs_in', exist_ok=True)
        os.makedirs('./tmp/txt', exist_ok=True)
        with open(f"./tmp/docs_in/{d['filename']}", 'wb') as f:
            f.write(d['content'])

    return raw_documents


@op(
    required_resource_keys={"blob_client"}
)
def store_converted_files(context, raw_documents: List[dict]):
    logger = context.log

    blob_client = context.resources.blob_client

    paths = [os.path.join('/opt/dagster/app/tmp/txt/', item) for item in os.listdir('./tmp/txt')]

    logger.info("Reading txt paths: %s", paths)
    raw_text_documents = []
    for p in paths:
        with open(p, 'rb') as f:
            raw_text_doc = {
                'filename': Path(f.name).name,
                'content': f.read()
            }
            raw_text_documents.append(raw_text_doc)

    for td in raw_text_documents:
        for rd in raw_documents:
            if Path(rd['filename']).stem == Path(td['filename']).stem:
                td['meta'] = rd['meta']

    logger.info("Putting %s raw_text_documents to blob store", len(raw_text_documents))
    for d in raw_text_documents:
        filename_path = Path(d['filename'])
        file_extension = filename_path.suffix
        filename_stem = filename_path.stem
        key = f"{filename_stem}/text{file_extension}"
        blob_client.put(key, d['content'])

    return raw_text_documents



@op(
    config_schema={"document_ids": Array(int)},
    required_resource_keys={"raw_documents_repository"}
)
def get_raw_documents(context):
    logger = context.log

    document_ids = context.op_config['document_ids']

    raw_documents_repository = context.resources.raw_documents_repository

    logger.info("Processing documents for ids %s", document_ids)
    raw_documents = raw_documents_repository.get_by_ids(document_ids)
    logger.info(raw_documents)
    logger.info(
        "Found %s documents to process: %s",
        len(raw_documents),
        [d['document_id'] for d in raw_documents]
    )

    for d in raw_documents:
        d['meta'] = {'document_id': d['document_id']}

    return raw_documents


@op(
    required_resource_keys={"raw_documents_repository"}
)
def update_documents(context, ml_documents: List[dict]):
    logger = context.log

    raw_documents_repository = context.resources.raw_documents_repository

    logger.info("Updating domain with %s MLDocuments: %s", len(ml_documents), ml_documents)
    response = raw_documents_repository.update_documents(ml_documents)
    logger.info("Update response: %s", response.status_code)

    return ml_documents


@op(
    required_resource_keys={"document_store", "preprocessor"}
)
def preprocess_raw_documents(context, raw_text_documents: List[dict]):
    logger = context.log

    document_store = context.resources.document_store
    preprocessor = context.resources.preprocessor

    for document in raw_text_documents:
        document['content'] = document['content'].decode('utf-8')

    preprocessed_docs = preprocessor.process(raw_text_documents)
    logger.info(
        "Preprocessed %s raw_documents into %s preprocessed docs",
        len(raw_text_documents),
        len(preprocessed_docs)
    )


    return preprocessed_docs


@op(
    required_resource_keys={"document_store"}
)
def save_ml_documents_to_document_store(context, preprocessed_documents: List[dict]):
    logger = context.log

    document_store = context.resources.document_store

    for doc in preprocessed_documents:
        doc['id'] = md5(doc['content'].encode('utf-8')).hexdigest()

    document_store.write_documents(preprocessed_documents)
    logger.info(
        "Updating documents with %s MLDocuments: %s",
        len(preprocessed_documents),
        [d['id'] for d in preprocessed_documents]
    )

    return preprocessed_documents


@op(
    config_schema={
        "query": str,
        "top_k": int
    },
    required_resource_keys={"reader"}
)
def refine_candidates(context, candidate_documents: List[MLDocument]):
    logger = context.log

    query = context.op_config['query']
    top_k = context.op_config['top_k']

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
def retrieve_candidates(context):
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
