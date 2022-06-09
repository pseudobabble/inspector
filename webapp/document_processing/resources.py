import json
import logging
import os
import time
from datetime import datetime
from uuid import uuid4, UUID

import flask
from flask import request
from flask_restful import Resource
from marshmallow import Schema

from infrastructure.dagster_client import DagsterClient, default_client
from infrastructure.repository import transaction

from .models import Query
from .builder import DocumentBuilder
from .job_execution import semantic_search
from .repository import DocumentRepository, QueryRepository
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
        if not uploaded_files:
            return {
                "error": "No file was provided, files must have the key 'file'"
            }, 422
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
    """
    Query result ingestion via webhook
    """

    routes = ["/hooks/semantic-search"]

    @transaction
    def post(self):
        body = request.get_json()
        run_id = body.get('run_id')
        query = QueryRepository().get_by_run_id(run_id)
        return query.answers, 201


class UserQuery(Resource):
    """
    NOTES:

    This could become a generic way for query runs to be triggered, depending on the
    endpoint schema.

    I think it would be better to use our own abstraction over
    the terminology that dagster uses, e.g. UserQuery or something. If there are
    other types of run that the user configures, they should probably use a
    different endpoint.

    """

    routes = ["/queries", "/queries/<int:query_id>"]

    def post(self):
        """
        Triggers a semantic_search, in keeping with REST, it returns the id of the created query.
        """
        client = default_client()
        body = request.get_json()

        # the example values
        args = {
            "topic outside",
            "lots of processes interface with resources outside of their silicon prison",
        }
        user_params = body.get("params")
        if user_params:
            args = user_params
            _logger.info(f"Initiating query with user supplied arguments: {args}")

        run_id = client.submit_job_execution(
            "answer_query", run_config=semantic_search.run_config(*args)
        )

        query = Query(run_id=UUID(run_id), answers={})
        QueryRepository().save(query)

        return {"query_id": str(query.id)}, 201

    def get(self, query_id=None):
        """
        Returns the answers to the user query with the id specified.
        :return: The content of the answers.
        """
        start = datetime.now()
        if query_id is None:
            return "", 404

        _logger.info(
            f"Received long polling request for results of query with id {query_id}"
        )

        query = None
        while not query:
            query = QueryRepository().get_by_id(str(query_id))
            time.sleep(5)
            if (datetime.now() - start).seconds > 20:
                return "", 404

        return {
            "content": json.loads(query.answers),
            "date": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        }
