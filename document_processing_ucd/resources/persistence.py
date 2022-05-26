from dagster import resource
from haystack.document_stores import SQLDocumentStore


@resource(config_schema={"url": str})
def sql_document_store(init_context):
    return SQLDocumentStore(url=init_context.resource_config["url"])
