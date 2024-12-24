from dagster import Field, Noneable, resource

from infrastructure.experiment_tracker import ExperimentTracker
from infrastructure.trackers.mlflow_tracker import MLFlowTracker

ExperimentTracker.trackers = {MLFlowTracker.__name__: MLFlowTracker}


@resource(
    config_schema={
        "tracker": str,
        **{
            tracker_config_name: Field(Noneable(tracker.resource_config.get_config()))
            for tracker_config_name, tracker in ModelTracker.trackers.items()
        },
    }
)
def experiment_tracker(init_context):
    config = init_context.resource_config

    tracker_name = config["tracker"]
    tracker_override_config = config[tracker_name]

    return ExperimentTracker(tracker_name, override_init_config=tracker_override_config)
