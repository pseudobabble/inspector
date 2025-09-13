import json
from dataclasses import asdict, dataclass


@dataclass
class RunContext:
    """
    An object to store transient but run-related things.
    """

    experiment_name: Optional[str] = None
    experiment_description: Optional[str] = None
    experiment_id: Optional[str] = None
    run_name: Optional[str] = None
    run_id: Optional[str] = None

    def to_dict(self):
        """Convert RunContext to a dictionary."""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict):
        """Recreate RunContext from a dictionary."""
        return RunContext(**data)

    def to_json(self):
        """Convert RunContext to a JSON string."""
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(data: str):
        """Recreate RunContext from a JSON string."""
        return RunContext.from_dict(json.loads(data))
