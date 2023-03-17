from dataclasses import dataclass

from pandas import DataFrame
from datasets import Dataset

from infrastructure.service import ServiceConfig

@dataclass
class ToHFDatasetConfig(ServiceConfig):
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


class ToHFDataset:
    """
    This class is designed to provide a common interface for all data processors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    resource_config = ToHFDatasetConfig

    def process(self, csv_bytesIO, *args, **kwargs):
        wrapper = io.TextIOWrapper(data, encoding='utf-8')
        df = pd.read_csv(wrapper)

        dataset = Dataset.from_pandas(dataframe)

        return dataset
