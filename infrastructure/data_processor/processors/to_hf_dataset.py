from dataclasses import dataclass

from pandas import DataFrame
from datasets import Dataset

from infrastructure.data_processor import (
    DataProcessorConfig,
    DataProcessor
)

@dataclass
class ToHFDatasetConfig(DataProcessorConfig):
    """
    This class is designed to hold DataProcessor __init__ configuration.

    The class will be used like:

    ```
    processor_config = DataProcessorConfig(
        some_kwarg=some_value,
        etc=etc
    )
    processor = MyDataProcessor.configure(**processor_config)
    ```
    """


class ToHFDataset(DataProcessor):
    """
    This class is designed to provide a common interface for all data processors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    def process(self, dataframe: DataFrame, *args, **kwargs):
        return Dataset.from_pandas(dataframe)
