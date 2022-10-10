import io
from dataclasses import dataclass
import csv
from collections import namedtuple

import pandas as pd

from infrastructure.service import (
    ServiceConfig
)

Dataset = namedtuple('Dataset', ('train', 'evaluate'))
TrainSplit = namedtuple('TrainSplit', ('X', 'y'))
EvalTestSplit = namedtuple('EvalTestSplit', ('y'))

@dataclass
class CsvToDatasetProcessorConfig(ServiceConfig):
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

    resource_config = CsvToDatasetProcessorConfig

    def process(self, data, *args, **kwargs):
        wrapper = io.TextIOWrapper(data, encoding='utf-8')
        df = pd.read_csv(wrapper, delimiter=';')

        eval_df = df.sample(frac=0.3)
        train_df = df.drop(index=eval_df.index)
        dataset = Dataset(
            train=TrainSplit(
                X=list(zip(train_df['residual sugar'], train_df['fixed acidity'])),
                y=train_df['quality']
            ),
            evaluate=EvalTestSplit(y=eval_df['quality'])
        )

        return dataset
