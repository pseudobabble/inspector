"""This module is the top level for document processing pipeline code"""
from dagster import job, repository

from resources.adaptor import data_adaptor
from resources.repository import model_repository
from resources.processor import data_processor
from resources.trainer import model_trainer

from graphs.training import train as train_graph


train = train_graph.to_job(
    resource_defs={
        'sklearn_model_repository': model_repository,
        's3_model_repository': model_repository,
        'data_adaptor': data_adaptor,
        'model_trainer': model_trainer,
        'data_processor': data_processor
    }
)


@repository
def training():
    return [
        train
    ]
