import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
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
    def from_env(cls):
        # TODO: field names need to be same as env names, fix
        return cls(**{
            key: value
            for key, value in dict(os.environ).items()
            if key in fields(cls)
        })

    @classmethod
    def from_dict(cls, config: dict):
        return cls(**{
            key: value
            for key, value in config.items()
            if key in fields(cls)
        })

    @classmethod
    def get_config(cls):
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
