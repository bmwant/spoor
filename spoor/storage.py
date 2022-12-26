from abc import ABC, abstractmethod
from collections import Counter
from typing import List


class Storage(ABC):
    @abstractmethod
    def get_value(self):
        raise NotImplemented("Provide implementation")

    @abstractmethod
    def get_name(self, key):
        raise NotImplemented("Provide implementation")

    @abstractmethod
    def set_name(self, key, name):
        raise NotImplemented("Provide implementation")

    @abstractmethod
    def inc(self, key):
        raise NotImplemented("Provide implementation")

    @abstractmethod
    def most_common(self, top_n: int = 3) -> List[tuple[str, int]]:
        raise NotImplemented("Provide implementation")


class MemoryStorage(Storage):
    def __init__(self):
        # TODO: add lock for thread safety
        self._registry = Counter()
        self._names = {}

    def get_value(self, key):
        return self._registry[key]

    def inc(self, key):
        self._registry[key] += 1

    def get_name(self, key) -> str:
        return self._names[key]

    def set_name(self, key, name: str):
        self._names[key] = name

    def most_common(self, top_n: int = 3):
        result = []
        for key, value in self._registry.most_common(n=top_n):
            name = self.get_name(key)
            result.append((name, value))
        return result
