import json
import logging
import os
import time
from datetime import datetime

import flask
from flask import request
from flask_restful import Resource
from infrastructure.dagster_client import DagsterClient, default_client
from infrastructure.repository import transaction
from marshmallow import Schema

from .builder import DocumentBuilder
from .job_execution import semantic_search
from .repository import DocumentRepository
from .schemata import Document, DocumentToPipeline, PipelineToMLDocument, RawDocument

_logger = logging.getLogger(__package__)


class Documents(Resource):
    """
    The Documents resource represents the ways that Document objects can be
    retrieved from the api
    """

    routes = ["/documents", "/documents/string:id"]

    def __init__(
        self,
        document_builder: DocumentBuilder = DocumentBuilder(),
        document_schema: Schema = Document(),
        document_repository: DocumentRepository = DocumentRepository(),
        raw_document_schema: RawDocument = RawDocument(),
        document_to_pipeline_schema: DocumentToPipeline = DocumentToPipeline(),
        pipeline_to_ml_document_schema: PipelineToMLDocument = PipelineToMLDocument(),
    ):
        self.document_builder = document_builder
        self.document_schema = document_schema
        self.document_repository = document_repository
        self.raw_document_schema = raw_document_schema
        self.document_to_pipeline_schema = document_to_pipeline_schema
        self.pipeline_to_ml_document_schema = pipeline_to_ml_document_schema

    def get(self) -> dict:
        """
        Retrieve Documents from the Documents resource by various parameters
        :param title: str
        :param timestamp: datetime
        :param latest: str
        :return: dict
        """
        request_args = flask.request.args
        if request_args.get("ids"):
            document_ids = json.loads(request_args["ids"])
            documents = self.document_repository.get_by_ids(document_ids)
            many = isinstance(documents, list)
            documents_response = self.document_to_pipeline_schema.dump(
                documents, many=many
            )
        else:
            documents = self.document_repository.get_all()
            many = isinstance(documents, list)
            documents_response = self.document_schema.dump(documents, many=many)

        return documents_response

    @transaction
    def post(self) -> None:
        """
        Create Documents by receiving POST requests with data specified as JSON
        in the request body
        :return: dict
        """
        data_dict = flask.request.get_json()
        many = isinstance(data_dict, list)
        raw_document = self.raw_document_schema.load(data_dict, many=many)
        try:
            document = self.document_builder.build(raw_document)

            response = self.document_schema.dump(document)
        except Exception as e:  # TODO
            response = {f"Exception: {e}": 400}

        return response

    @transaction
    def patch(self):
        """
        Update Documents by receiving POST requests with data specified as JSON
        in the request body
        TODO: needs to be made into a proper resource
        :return: dict
        """
        data_dict = flask.request.get_json()
        many = isinstance(data_dict, list)  # TODO: fix naming here
        documents = self.document_builder.update_documents_with_ml_documents(data_dict)
        response = self.document_schema.dump(documents, many=many)

        return response


class Upload(Resource):

    routes = ["/documents/upload"]

    def __init__(
        self,
        document_builder: DocumentBuilder = DocumentBuilder(),
        document_repository: DocumentRepository = DocumentRepository(),
        dagster_client: DagsterClient = DagsterClient(),
    ):
        self.document_builder = document_builder
        self.document_repository = document_repository
        self.dagster_client = dagster_client

    @transaction
    def post(self):
        uploaded_files = flask.request.files.getlist("file")
        file_data = [
            {"filename": f.filename, "content": f.read()} for f in uploaded_files
        ]

        document_ids = []
        for datum in file_data:
            document = self.document_builder.build(
                {"filename": datum["filename"], "content": datum["content"]}
            )
            document_ids.append(document.id)
            print(document.raw_content)

        return {"success": 200}


class AnswerHook(Resource):
    routes = ["/hooks/semantic-search"]

    @transaction
    def post(self):
        body = request.get_json()
        with open("/tmp/answers.json", "w") as file:
            json.dump(body, file, indent=4)
        return {"success": 200}


class DataUpdate(Resource):
    routes = ["/semantic-search/results"]

    def get(self):
        """
        Returns 'data.txt' content when the resource has
        changed after the request time
        """
        while not os.path.exists("/tmp/answers.json"):
            _logger.warning("checking for answers.json")
            time.sleep(0.5)

        _logger.warning("WOHOOOOO found it, sending...")

        with open("/tmp/answers.json", "r") as data:
            content = data.read()

        _logger.warning("deleting the old file")
        os.unlink("/tmp/answers.json")

        _logger.critical("SUCCESS")
        return {
            "content": content,
            "date": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        }


json_ = """
{
  "ops": {
    "retrieve_candidates": {
      "config": {
        "query": "topic outside ",
        "top_k": 30
      }
    },
    "semantic_refine_candidates": {
      "config": {
        "query": "lots of processes interface with resources outside of their silicon prison",
        "top_k": 2
      }
    }
  },
  "resources": {
    "document_store": {
      "config": {
        "url": "postgresql://webapp_postgres_user:webapp_postgres_password@webapp-postgres:5432/document_store"
      }
    },
    "reader": {
      "config": {
        "model_name": "deepset/roberta-base-squad2",
        "use_gpu": true
      }
    },
    "answer_client": {
      "config": {
        "url": "http://172.17.0.1:80/api/hooks/semantic-search"
      }
    }
  }
}
"""


class Trigger(Resource):
    routes = ["/trigger"]

    def get(self):
        """dev method to trigger runs"""
        config = {}
        config["run_config"] = json.loads(json_)
        client = default_client()
        config.update(
            {
                # "job_name": "answer_query",
                # "repository_location_name": "dagster-ucd-document-processing",
                # "repository_name": "__repository__answer_query",
                # "mode": "default"
            }
        )

        client.submit_job_execution(
            "answer_query", run_config=semantic_search.run_config()
        )
        #    job_name=config['job_name'],
        #    repository_location_name=config['repository_location_name'],
        #    repository_name=config['repository_name'],
        #    run_config=config['run_config'],
        #    mode=config['mode']
        # )
