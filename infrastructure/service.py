from abc import ABC, abstractmethod
from dataclasses import dataclass
import inspect


@dataclass
class ServiceConfig:

    @classmethod
    def from_dict(cls, config: dict):
        return cls(**{
            key: value
            for key, value in env.items()
            if key in inspect.signature(cls).parameters
        })

    @classmethod
    def get_resource_config(cls):
        parameters = inspect.signature(cls).parameters

        return {
            name: parameter.annotation
            for name, parameter in parameters.items()
        }


class Service(ABC):

    @abstractmethod
    @classmethod
    def configure(cls, config: ServiceConfig) -> 'Service':
        return cls(config)
