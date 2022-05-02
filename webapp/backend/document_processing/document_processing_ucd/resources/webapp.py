import json
from typing import List

import requests
from dagster import resource

from schemata import DocumentToPipeline, PipelineToMLDocument, MLDocument


class RawDocumentsRepository:

    def __init__(
            self,
            url,
            client = requests,
            pipeline_to_document_schema = PipelineToMLDocument(),
            document_to_pipeline_schema = DocumentToPipeline()
    ):
        self.url = url
        self.client = client
        self.pipeline_to_document_schema = pipeline_to_document_schema
        self.document_to_pipeline_schema = document_to_pipeline_schema

    def get_by_ids(self, document_ids: List[int]):
        documents_response = self.client.get(
            self.url,
            params={"ids": json.dumps(document_ids)}
        )

        print(documents_response)

        raw_documents = self.document_to_pipeline_schema.load(
            [d for d in documents_response.json()],
            many=True
        )

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
    return RawDocumentsRepository(init_context.resource_config['url'])
