from dagster import op


@op(
    config_schema={"document_ids": Array(int)},
    required_resource_keys={"document_store", "raw_documents_repository"}
)
def get_raw_documents(context):
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

    return raw_documents

@op(
    required_resource_keys={"raw_documents_repository"}
)
def update_documents(ml_documents: List[MLDocument]):
    response = raw_documents_repository.update_documents(ml_documents)
    logger.info("Update response: %s", response.status_code)

    return preprocessed_docs
