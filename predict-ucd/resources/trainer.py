from dagster import Field, Noneable, resource
from services.trainers.sklearn_trainer import SKLearnTrainer

from infrastructure import ModelTrainer

ModelTrainer.trainers = {SKLearnTrainer.__name__: SKLearnTrainer}


@resource(
    config_schema={
        "trainer": str,
        **{
            trainer_config_name: Field(Noneable(trainer.resource_config.get_config()))
            for trainer_config_name, trainer in ModelTrainer.trainers.items()
        },
    }
)
def model_trainer(init_context):
    config = init_context.resource_config

    trainer_name = config["trainer"]
    trainer_override_config = config[trainer_name]

    return ModelTrainer(trainer_name, override_init_config=trainer_override_config)
