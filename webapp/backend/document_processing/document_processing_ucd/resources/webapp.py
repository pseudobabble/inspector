import json
from typing import List

import requests
from dagster import resource

from schemata import PipelineToMLDocument


class RawDocumentsRepository:

    def __init__(
            self,
            dagster_init_context,
            client = requests,
            pipeline_to_document_schema = PipelineToMLDocument()
    ):
        self.url = dagster_init_context.resource_config.get('url')
        self.client = client
        self.pipeline_to_document_schema = pipeline_to_document_schema

    def get_by_ids(self, document_ids: List[int]):
        documents_response = self.client.get(
            self.url,
            params={"ids": json.dumps(document_ids)}
        )

        raw_documents = [d for d in documents_response.json()]

        return raw_documents

    def update_documents(self, ml_documents: List[MLDocument]):
        # TODO: do we want to keep sending the whole document, or just ids?
        update_response = self.client.patch(
            self.url,
            json=self.pipeline_to_document_schema.dump(ml_documents, many=True)
        )

        return update_response


@resource(config_schema={"url": str})
def raw_documents_repository(init_context):
    return RawDocumentsRepository(init_context)
