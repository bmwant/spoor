from abc import ABC, abstractmethod
from collections import Counter


class Storage(ABC):
    @abstractmethod
    def get_value(self):
        raise NotImplemented("Provide implementation")

    @abstractmethod
    def inc(self, key):
        raise NotImplemented("Provide implementation")


class MemoryStorage(Storage):
    def __init__(self):
        # TODO: add lock for thread safety
        self._registry = Counter()

    def get_value(self, key):
        return self._registry[key]

    def inc(self, key):
        self._registry[key] += 1
