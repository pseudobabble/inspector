"""This module is the top level for document processing pipeline code"""
from dagster import job, repository
from graphs.predict import predict as predict_graph
from resources.adaptor import data_adaptor
from resources.converter import model_converter
from resources.processor import data_processor
from resources.repository import model_repository
from resources.trainer import model_trainer

# from dagster_mlflow import mlflow_tracking, end_mlflow_on_run_finished


predict = predict_graph.to_job(
    resource_defs={
        "get_model_repository": model_repository,
        "data_adaptor": data_adaptor,
        "data_processor": data_processor,
        #        'mlflow': mlflow_tracking
    }
)


@repository
def prediction():
    return [predict]
