import inspect
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Any, Optional


@dataclass
class ServiceConfig:
    """
    This class is designed to be a DTO for Service
    configuration.

    If the service is used as a @resource, this config
    can be converted into a typed dict for the @resource
    config schema.
    """

    ENV_PREFIX: str

    @classmethod
    def from_env(cls):
        init_args = {field.name for field in fields(cls) if field.init}

        return cls(
            **{
                key: value
                for key, value in dict(os.environ).items()
                if key.strip(cls.ENV_PREFIX) in fields(cls)
            }
        )

    @classmethod
    def from_dict(cls, config: dict):
        init_args = {field.name for field in fields(cls) if field.init}

        return cls(**{key: value for key, value in config.items() if key in init_args})

    @classmethod
    def get_config(cls):
        parameters = inspect.signature(cls).parameters

        return {name: parameter.annotation for name, parameter in parameters.items()}


class Service(ABC):
    """
    This class provides an interface for a configurable Service.

    Instance configuration can be provided via @resource config,
    defined by a ServiceConfig, and method parametrisation can be
    achieved with @op config, which is then passed to the service
    method called in the @op.
    """


@dataclass
class ServiceResult:
    """
    This class provides an interface for the result of a service execution.

    Subclass this class and implement any methods required by receivers.
    """

    result: Optional[Any]
