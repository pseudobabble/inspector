from datetime import datetime
import json

import flask
from flask_restful import Resource
from marshmallow import Schema

from infrastructure.dagster_client import DagsterClient
from infrastructure.repository import transaction
from .builder import DocumentBuilder
from .schemata import Document, RawDocument, MLDocument, DocumentToPipeline
from .repository import DocumentRepository


class Documents(Resource):
    '''
    The Documents resource represents the ways that Document objects can be
    retrieved from the api
    '''
    routes = [
        "/documents",
        "/documents/string:id"
    ]

    def __init__(
            self,
            document_builder: DocumentBuilder = DocumentBuilder(),
            document_schema: Schema = Document(),
            document_repository: DocumentRepository = DocumentRepository(),
            raw_document_schema: RawDocument = RawDocument(),
            document_to_pipeline_schema: DocumentToPipeline = DocumentToPipeline()
    ):
        self.document_builder = document_builder
        self.document_schema = document_schema
        self.document_repository = document_repository
        self.raw_document_schema = raw_document_schema
        self.document_to_pipeline_schema = document_to_pipeline_schema

    def get(self) -> dict:
        """
        Retrieve Documents from the Documents resource by various parameters
        :param title: str
        :param timestamp: datetime
        :param latest: str
        :return: dict
        """
        request_args = flask.request.args
        if request_args.get('ids'):
            document_ids = json.loads(request_args['ids'])
            documents = self.document_repository.get_by_ids(document_ids)
            many = len(documents) > 1
            documents_response = self.document_to_pipeline_schema.dump(documents, many=many)
        else:
            documents = self.document_repository.get_all()
            many = len(documents) > 1
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
        raw_document = self.raw_document_schema.load(data_dict)
        try:
            document = self.document_builder.build(raw_document)
            response = self.document_schema.dump(document)
        except Exception as e: # TODO
            raise e
            response = {
                f"Exception: {e}": 400
            }

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
        many = len(data_dict) > 1
        #ml_document_data = self.pipeline_to_ml_document_schema.load(data_dict, many=many)
        try:
            documents = self.document_builder.update_documents_with_ml_documents(data_dict)
            response = self.document_schema.dump(documents, many=many)
        except Exception as e: # TODO
            raise e

        return response

class Trigger(Resource):
    routes = ['/trigger']
    def post(self):
        """dev method to trigger runs"""
        config = flask.request.get_json()
        client = DagsterClient()

        client.trigger_run(
            job_name=config['job_name'],
            repository_location_name=config['repository_location_name'],
            repository_name=config['repository_name'],
            run_config=config['run_config'],
            mode=config['mode']
        )
