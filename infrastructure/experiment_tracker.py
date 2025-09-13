from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from infrastructure.service import Service, ServiceConfig, ServiceResult


@dataclass
class TrackerConfig(ServiceConfig):
    """
    This class is designed to hold Processor __init__ configuration.

    The class will be used like:

    ```
    processor_config = ProcessorConfig(
        some_kwarg=some_value,
        etc=etc
    )
    processor = MyProcessor(trainer_config)
    ```
    """


class Tracker(ABC):
    """
    This class is designed to provide a common interface for all DataProcessors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    resource_config = Optional[TrackerConfig]

    @abstractmethod
    def create_experiment(self, experiment_name: str):
        """Create a new experiment and set it as active."""
        raise NotImplementedError(
            "You must implement `create_experiment` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def start_run(self, experiment_id: Any, run_name: str):
        """Start a new run within the current experiment."""
        raise NotImplementedError(
            "You must implement `start_run` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_metric(self, run_id: Any, name: str, value: float, step: int = None):
        """Log a single metric."""
        raise NotImplementedError(
            "You must implement `log_metric` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_metrics(self, run_id: Any, metrics: dict, step: int = None):
        """Log multiple metrics."""
        raise NotImplementedError(
            "You must implement `log_metrics` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_parameter(self, run_id: Any, name: str, value: Any):
        """Log a single parameter."""
        raise NotImplementedError(
            "You must implement `log_parameter` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_parameters(self, run_id: Any, parameters: dict):
        """Log multiple parameters."""
        raise NotImplementedError(
            "You must implement `log_parameters` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_artifact(self, run_id: Any, name: str, artifact: Any):
        """Log an artifact (e.g., model checkpoint, plots)."""
        raise NotImplementedError(
            "You must implement `log_artifact` on {self.__class__.__name__}`"
        )


class ExperimentTracker(Service):
    trackers = {}

    def __init__(
        self,
        tracker_name: str,
        state_store: RedisStateStore,
        override_init_config: Optional[dict] = None,
    ):
        """
        Initialize the ExperimentTracker.

        Args:
            tracker_name (str): Name of the backend tracker to use.
            state_store (RedisStateStore): Redis-based state store for managing experiment/run IDs.
            override_init_config (dict, optional): Configuration overrides for the backend tracker.
        """
        tracker = self.trackers[tracker_name]
        self.state_store = state_store
        if override_init_config:
            tracker_config = tracker.resource_config.from_dict(override_init_config)
            self.tracker = tracker(tracker_config)
        else:
            self.tracker = tracker()

    def create_experiment(
        self,
        experiment_name: str,
        user_id: str = "",
        pipeline_id: str = "",
        description: str = None,
    ) -> str:
        """
        Create an experiment and persist its ID in Redis.

        Args:
            experiment_name (str): Name of the experiment.
            user_id (str): Optional user ID.
            pipeline_id (str): Optional pipeline ID.
            description (str, optional): Description of the experiment.

        Returns:
            str: The experiment ID.
        """
        experiment_id = self.tracker.create_experiment(experiment_name, description)
        self.state_store.save_experiment_id(
            experiment_name, experiment_id, user_id, pipeline_id
        )
        return experiment_id

    def start_run(
        self,
        experiment_name: str,
        run_name: str,
        user_id: str = "",
        pipeline_id: str = "",
        tags: dict = None,
    ) -> str:
        """
        Start a new run and persist its ID in Redis.

        Args:
            experiment_name (str): Name of the experiment.
            run_name (str): Name of the run.
            user_id (str): Optional user ID.
            pipeline_id (str): Optional pipeline ID.
            tags (dict, optional): Tags for the run.

        Returns:
            str: The run ID.
        """
        experiment_id = self.state_store.get_experiment_id(
            experiment_name, user_id, pipeline_id
        )
        if not experiment_id:
            raise ValueError(f"Experiment '{experiment_name}' does not exist.")

        run_id = self.tracker.start_run(experiment_id, run_name, tags)
        self.state_store.save_run_id(run_name, run_id, user_id, pipeline_id)
        return run_id

    def log_metric(
        self,
        run_name: str,
        name: str,
        value: float,
        user_id: str = "",
        pipeline_id: str = "",
        step: int = None,
    ):
        """
        Log a single metric to the run.

        Args:
            run_name (str): Name of the run.
            name (str): Metric name.
            value (float): Metric value.
            user_id (str): Optional user ID.
            pipeline_id (str): Optional pipeline ID.
            step (int, optional): Metric step.
        """
        run_id = self.state_store.get_run_id(run_name, user_id, pipeline_id)
        if not run_id:
            raise ValueError(f"Run '{run_name}' does not exist.")

        self.tracker.log_metric(run_id, name, value, step)

    def log_parameter(
        self,
        run_name: str,
        name: str,
        value: Any,
        user_id: str = "",
        pipeline_id: str = "",
    ):
        """
        Log a single parameter to the run.

        Args:
            run_name (str): Name of the run.
            name (str): Parameter name.
            value (Any): Parameter value.
            user_id (str): Optional user ID.
            pipeline_id (str): Optional pipeline ID.
        """
        run_id = self.state_store.get_run_id(run_name, user_id, pipeline_id)
        if not run_id:
            raise ValueError(f"Run '{run_name}' does not exist.")

        self.tracker.log_parameter(run_id, name, value)
