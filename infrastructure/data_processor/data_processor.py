from dataclasses import dataclass

from .service import Service, ServiceConfig


class DataProcessor(Service):
    """
    This class is designed to provide a common interface for all data processors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    processors = {
        'to_hf'
    }

    def __init__(self, processor_name: str, override_init_config: Optional[dict] = None):
        processor = self.processors[processor_name]
        processor_config = processor.config.from_dict(override_init_config)

        if override_init_config:
            self.processor = processor(processor_config)
        else:
            self.processor = processor()

    def process(self, data, *args, **kwargs):
        return self.processor.process(data, args, kwargs)
