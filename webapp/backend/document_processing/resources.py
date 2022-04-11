from datetime import datetime
import json

import flask
from flask_restful import Resource
from marshmallow import Schema

from infrastructure.dagster_client import DagsterClient
from infrastructure.repository import transaction
from .builder import DocumentBuilder
from .schemata import DocumentSchema
from .repository import DocumentRepository
from .models import RawDocument

import logging
logging.basicConfig(filename='example.log')

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
            document_schema: Schema = DocumentSchema(),
            document_repository: DocumentRepository = DocumentRepository()
    ):
        """
        This method initialises the Documents resource with it's dependencies
        :param document_builder: DocumentBuilder
        :param document_repository: BaseAdaptor
        :param document_schema: Schema
        """
        self.document_builder = document_builder
        self.document_schema = document_schema
        self.document_repository = document_repository


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
            self.document_schema.many = True
            documents = self.document_repository.get_by_ids(json.loads(request_args['ids']))
        else:
            documents = self.document_repository.get_all()

        documents_response = self.document_schema.dump(documents)

        return documents_response

    def get_by_ids(self) -> dict:
        data_dict = flask.request.get_json()
        documents = self.document_repository.get_by_ids(data_dict['ids'])
        documents_response = [
            self.document_schema.dump(document)
            for document in documents
        ]

        return documents_response

    @transaction
    def post(self) -> None:
        """
        Create Documents by receiving POST requests with data specified as JSON
        in the request body
        :return: dict
        """
        data_dict = flask.request.get_json()
        try:
            raw_document = RawDocument(
                filename=data_dict['filename'],
                content=data_dict['content']
            )
            document = self.document_builder.build(raw_document)
            response = self.document_schema.dump(document)
        except Exception as e: # TODO
            raise e
            response = {
                f"Exception: {e}": 400
            }

        return response

    @transaction
    def upload(self):
        if flask.request.method == "POST":
            files = flask.request.files.getlist("file")
            raw_docs = [RawDocument(filename=f.filename, content=f.read()) for f in files]
            documents = [self.document_builder.build(doc) for doc in raw_docs]
            response_documents = [self.document_schema.dump(document) for document in documents]

            return response_documents

    @transaction
    def patch(self):
        """
        Update Documents by receiving POST requests with data specified as JSON
        in the request body
        TODO: needs to be made into a proper resource
        :return: dict
        """
        data_dict = json.loads(flask.request.get_json())
        try:
            documents = self.document_builder.update_documents_with_ml_documents(data_dict)
            response = {'success': 200}
        except Exception as e: # TODO
            raise e
            response = {
                f"Exception: {e}": 400
            }

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
