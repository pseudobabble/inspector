"""This module is the top level for document processing pipeline code"""
from dagster import job, repository

from resources.model_repo import model_repository
from resources.data_adaptor import data_adaptor
from resources.trainer import trainer
from graphs.training import train as train_graph


train = train_graph.to_job(
    resource_defs={
        'hf_model_repository': hf_model_repository,
        's3_model_repository': s3_model_repository,
        'data_adaptor': s3_data_adaptor,
        'trainer': hf_trainer,
        'data_processor': to_hf_dataset
    }
)


@repository
def training():
    return [
        train
    ]
