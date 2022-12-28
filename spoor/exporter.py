from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import datadog


class Exporter(ABC):
    @abstractmethod
    def send(self, key: str, value: Any) -> None:
        raise NotImplemented("Provide implementation")

    @abstractmethod
    def flush(self) -> None:
        raise NotImplemented("Provide implementation")


class StatsdExporter(Exporter):
    pass


class DatadogExporter(Exporter):

    _DEFAULT_OPTIONS = {
        "statsd_host": "127.0.0.1",
        "statsd_port": 8125,
    }

    def __init__(
        self,
        *,
        options: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        prefix: Optional[str] = None,
    ):
        self.options = options or self._DEFAULT_OPTIONS
        self.tags = tags or []
        self.prefix = prefix
        datadog.initialize(**self.options)
        self.statsd = datadog.statsd

    def send(self, key, value):
        if self.prefix is not None:
            key = f"{self.prefix}.{key}"
        self.statsd.increment(key, tags=self.tags)

    def flush(self):
        print("Flushing when deleting")
        self.statsd.flush()
