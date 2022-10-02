"""This module is the top level for document processing pipeline code"""
from dagster import job, repository

from resources.model_repository import hf_model_repository, s3_model_repository
from resources.data_adaptor import s3_data_adaptor
from resources.data_processor import to_hf_dataset
from resources.trainer import hf_trainer
from graphs.training import train_pretrained as train_pretrained_graph


train_pretrained = train_pretrained_graph.to_job(
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
        train_pretrained
    ]
