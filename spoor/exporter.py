from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

import datadog


class Exporter(ABC):
    @abstractmethod
    def inc(self, key: str) -> None:
        raise NotImplemented("Provide implementation")
    
    @abstractmethod
    def flush(self) -> None:
        raise NotImplemented("Provide implementation")


class DatadogExporter(Exporter):

    _DEFAULT_OPTIONS = {
        "statsd_host": "127.0.0.1",
        "statsd_port": 8125,
    }

    def __init__(
        self, 
        options: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ):
        self.options = options or self._DEFAULT_OPTIONS
        self.tags = tags or []
        datadog.initialize(**self.options)
        self.statsd = datadog.statsd

    def inc(self, key):
        self.statsd.increment(key, tags=self.tags)

    def flush(self):
        self.statsd.flush()
