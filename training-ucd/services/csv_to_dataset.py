from dataclasses import dataclass
import csv
from collections import namedtuple

from pandas import DataFrame

from infrastructure.data_processor import (
    DataProcessorConfig,
    DataProcessor
)

@dataclass
class CsvToDatasetProcessorConfig(DataProcessorConfig):
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


class CsvToDatasetProcessor:
    """
    This class is designed to provide a common interface for all data processors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    def process(self, data, *args, **kwargs):
        Dataset = namedtuple('Dataset', ('train', 'evaluate', 'test'))
        Split = namedtuple('Split', ('X', 'y'))

        df = DataFrame.read_csv(data)
        train = Split(X=df.)

        return data
