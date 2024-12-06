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
        df = pd.read_csv(wrapper, delimiter=";")

        eval_df = df.sample(frac=0.3)
        train_df = df.drop(index=eval_df.index)
        dataset = Dataset(
            train=Split(
                X=array(
                    list(zip(train_df["residual sugar"], train_df["fixed acidity"]))
                ),
                y=train_df["quality"],
            ),
            evaluate=Split(
                X=array(list(zip(eval_df["residual sugar"], eval_df["fixed acidity"]))),
                y=eval_df["quality"],
            ),
        )

        return dataset
