from abc import ABC, abstractmethod


class Exporter(ABC):
    @abstractmethod
    def send(self, key: str, **extras) -> None:
        raise NotImplementedError("Provide implementation")

    @abstractmethod
    def flush(self) -> None:
        raise NotImplementedError("Provide implementation")
