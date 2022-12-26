from abc import ABC, abstractmethod

import datadog


class Exporter(ABC):
    @abstractmethod
    def inc(self, key: str) -> None:
        raise NotImplemented("Provide implementation")
    
    @abstractmethod
    def flush(self) -> None:
        raise NotImplemented("Provide implementation")


class DatadogExporter(Exporter):
    def __init__(self):
        options = {
            "statsd_host": "127.0.0.1",
            "statsd_port": 8125,
        }

        datadog.initialize(**options)
        self.statsd = datadog.statsd

    def inc(self, key):
        self.statsd.increment('example_metric.increment', tags=["environment:dev"])
        self.statsd.increment(key, tags=["environment:dev"])

    def flush(self):
        pass
