from abc import ABC, abstractmethod
from dataclasses import dataclass
import inspect


@dataclass
class ServiceConfig:
    """
    This class is designed to be a DTO for Service
    configuration.

    If the service is used as a @resource, this config
    can be converted into a typed dict for the @resource
    config schema.
    """

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
    """
    This class provides an interface for a configurable Service.

    Instance configuration can be provided via @resource config,
    defined by a ServiceConfig, and method parametrisation can be
    achieved with @op config, which is then passed to the service
    method called in the @op.
    """

    @classmethod
    @abstractmethod
    def configure(cls, config: ServiceConfig) -> 'Service':
        return cls(config)
