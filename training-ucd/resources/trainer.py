from dagster import resource

from services.model.hf_model_trainer import HFTrainer, HFTrainerConfig


@resource(config_schema=HFTrainerConfig.get_resource_config())
def hf_trainer(init_context):
    config = HFTrainerConfig.from_dict(init_context)
    return HFTrainer.configure(config)
