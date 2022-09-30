from abc import ABC, abstractmethod

class Service(ABC):

    @abstractmethod
    @classmethod
    def configure(cls, config: dict) -> 'Service':
        return cls(**config)
