"""This module is the top level for document processing pipeline code"""
from dagster import job, repository
from dagster_mlflow import mlflow_tracking, end_mlflow_on_run_finished

from resources.adaptor import data_adaptor
from resources.repository import model_repository
from resources.processor import data_processor
from resources.trainer import model_trainer
from resources.converter import model_converter

from graphs.training import train as train_graph
from graphs.predict import predict as predict_graph


train = train_graph.to_job(
    resource_defs={
        'get_model_model_repository': model_repository,
        'save_model_model_repository': model_repository,
        'data_adaptor': data_adaptor,
        'model_trainer': model_trainer,
        'data_processor': data_processor,
        'model_converter': model_converter,
        'mlflow': mlflow_tracking
    }
)

predict = predict_graph.to_job(
    resource_defs={
        'get_model_repository': model_repository,
        'data_adaptor': data_adaptor,
        'data_processor': data_processor,
        'mlflow': mlflow_tracking
    }
)


@repository
def training():
    return [
        train,
        predict
    ]
