from typing import Optional
from dataclasses import dataclass

from infrastructure.service import Service, ServiceConfig

from infrastructure.processors.to_hf_dataset import ToHFDataset
from infrastructure.processors.csv_to_dataset import CsvToDatasetProcessor


class DataProcessor(Service):
    """
    This class is designed to provide a common interface for all data processors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    processors = {
        ToHFDataset.__name__: ToHFDataset,
        CsvToDatasetProcessor.__name__: CsvToDatasetProcessor
    }

    def __init__(self, processor_name: str, override_init_config: Optional[dict] = None):
        processor = self.processors[processor_name]

        if override_init_config:
            processor_config = processor.resource_config.from_dict(override_init_config)
            self.processor = processor(processor_config)
        else:
            self.processor = processor()

    def process(self, data, *args, **kwargs):
        return self.processor.process(data, *args, **kwargs)
