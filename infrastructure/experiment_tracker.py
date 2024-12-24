from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

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
    def create_experiment(self, name: str, description: str = None):
        """Create a new experiment and set it as active."""
        raise NotImplementedError(
            "You must implement `create_experiment` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def set_experiment(self, experiment_id: str):
        """Switch to an existing experiment."""
        raise NotImplementedError(
            "You must implement `set_experiment` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def start_run(self, run_name: str = None, tags: dict = None):
        """Start a new run within the current experiment."""
        raise NotImplementedError(
            "You must implement `start_run` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_metric(self, name: str, value: float, step: int = None):
        """Log a single metric."""
        raise NotImplementedError(
            "You must implement `log_metric` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_metrics(self, metrics: dict, step: int = None):
        """Log multiple metrics."""
        raise NotImplementedError(
            "You must implement `log_metrics` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_parameter(self, name: str, value: Any):
        """Log a single parameter."""
        raise NotImplementedError(
            "You must implement `log_parameter` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_parameters(self, parameters: dict):
        """Log multiple parameters."""
        raise NotImplementedError(
            "You must implement `log_parameters` on {self.__class__.__name__}`"
        )

    @abstractmethod
    def log_artifact(self, name: str, artifact: Any):
        """Log an artifact (e.g., model checkpoint, plots)."""
        raise NotImplementedError(
            "You must implement `log_artifact` on {self.__class__.__name__}`"
        )


class ExperimentTracker(Service):
    """
    This class is designed to provide a common interface for all data processors.

    You should subclass this class for your use case, and implement the `process`
    method.
    """

    trackers = {}

    def __init__(self, tracker_name: str, override_init_config: Optional[dict] = None):
        tracker = self.trackers[tracker_name]

        if override_init_config:
            tracker_config = tracker.resource_config.from_dict(override_init_config)
            self.tracker = tracker(tracker_config)
        else:
            self.tracker = tracker()

    def create_experiment(self, name: str, description: str = None):
        """Create a new experiment and set it as active."""
        self.tracker.create_experiment(name, description)

    def set_experiment(self, experiment_id: str):
        """Switch to an existing experiment."""
        self.tracker.set_experiment(experiment_id)

    def start_run(self, run_name: str = None, tags: dict = None):
        """Start a new run within the current experiment."""
        self.tracker.start_run(run_name, tags)

    def log_metric(self, name: str, value: float, step: int = None):
        """Log a single metric."""
        self.tracker.log_metric(name, value, step)

    def log_metrics(self, metrics: dict, step: int = None):
        """Log multiple metrics."""
        self.tracker.log_metrics(metrics, step)

    def log_parameter(self, name: str, value: Any):
        """Log a single parameter."""
        self.tracker.log_parameter(name, value)

    def log_parameters(self, parameters: dict):
        """Log multiple parameters."""
        self.tracker.log_parameters(parameters)

    def log_artifact(self, name: str, artifact: Any):
        """Log an artifact (e.g., model checkpoint, plots)."""
        self.tracker.log_artifact(name, artifact)
