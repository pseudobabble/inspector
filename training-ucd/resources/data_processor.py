from dagster import resource

from services.processors.to_hf_dataset import ToHFDataset


@resource
def to_hf_dataset(init_context):
    return ToHFDataset()
