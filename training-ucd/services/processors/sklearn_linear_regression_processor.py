import csv
import io
from collections import namedtuple
from dataclasses import dataclass

import pandas as pd
from numpy import array

from infrastructure.service import ServiceConfig

Dataset = namedtuple("Dataset", ("train", "evaluate"))
Split = namedtuple("Split", ("X", "y"))


@dataclass
class SKLearnLinearRegressionProcessorConfig(ServiceConfig):
    """ """


class SKLearnLinearRegressionProcessor:
    """ """

    resource_config = SKLearnLinearRegressionProcessorConfig

    def process(self, data, *args, **kwargs):
        wrapper = io.TextIOWrapper(data, encoding="utf-8")
        df = pd.read_csv(wrapper)

        eval_df = df.sample(frac=0.3)
        train_df = df.drop(index=eval_df.index)
        dataset = Dataset(
            train=Split(
                X=train_df["bmi"].to_numpy().reshape(-1, 1),
                y=train_df["target"].to_numpy().reshape(-1, 1),
            ),
            evaluate=Split(
                X=train_df["bmi"].to_numpy().reshape(-1, 1),
                y=eval_df["target"].to_numpy().reshape(-1, 1),
            ),
        )

        return dataset
