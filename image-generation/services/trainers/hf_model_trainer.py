from dataclasses import dataclass

import evaluate
from datasets import Dataset
from transformers import AutoTokenizer, TrainingArguments, Trainer

from infrastructure.model_trainer import (
    ModelTrainerConfig,
    ModelTrainer
)

@dataclass
class HFTrainerConfig(ModelTrainerConfig):
    """
    This class is designed to hold Trainer __init__ configuration.

    The class will be used like:

    ```
    trainer_config = TrainerConfig(
        some_kwarg=some_value,
        etc=etc
    )
    trainer = MyTrainer.configure(trainer_config)
    ```
    """
    model_name: str


class HFTrainer(ModelTrainer):
    """
    This class is designed to provide a common interface for all data trainers.

    You should subclass this class for your use case, and implement the `train`
    method.
    """

    resource_config = HFTrainerConfig

    def train(self, model, dataset: Dataset, *args, **kwargs):
        # build tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        def tokenize(dataset):
            return tokenizer(examples["text"], padding="max_length", truncation=True)

        # tokenize
        tokenized_datasets = dataset.map(tokenize, batched=True)

        # build training args
        evaluator = evaluate.load("accuracy")
        def compute_metrics(eval_predictions):
            logits, labels = eval_pred
            predictions = np.argmax(logits, axis=-1)
            return evaluator.compute(predictions=predictions, references=labels)

        training_args = TrainingArguments(output_dir="test_trainer", evaluation_strategy="epoch")

        # init trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=small_train_dataset,
            eval_dataset=small_eval_dataset,
            compute_metrics=compute_metrics,
        )

        training_result = trainer.train()

        return model
