from dataclasses import dataclass
from typing import Optional

from infrastructure.service import Service, ServiceConfig, ServiceResult


class ProcessorResult(ServiceResult):
    """
    This class provices a common interface for all results of DataProcessor.process
    """


class Processor(ABC):
    """
    This class is designed to provide a common interface for all DataProcessors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    @abstractmethod
    def process(self, *args, **kwargs) -> ProcessorResult:
        raise NotImplementedError(
            "You must implement `process` on {self.__class__.__name__}`"
        )


class DataProcessor(Service):
    """
    This class is designed to provide a common interface for all data processors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    processors = {}

    def __init__(
        self, processor_name: str, override_init_config: Optional[dict] = None
    ):
        processor = self.processors[processor_name]

        if override_init_config:
            processor_config = processor.resource_config.from_dict(override_init_config)
            self.processor = processor(processor_config)
        else:
            self.processor = processor()

    # TODO: use this pattern elsewhere
    def process(self, data: ServiceResult, *args, **kwargs):
        if not data.result:
            # TODO: see below
            raise RuntimeError("Replace me with a better message")
        processed_data = self.processor.process(data, *args, **kwargs)
        return ProcessorResult(result=processed_data)
