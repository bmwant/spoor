from abc import ABC, abstractmethod

import datadog


class Exporter(ABC):
    @abstractmethod
    def flush(self):
        raise NotImplemented("Provide implementation")


class DatadogExporter(Exporter):
    def __init__(self):
        options = {
            'statsd_host':'127.0.0.1',
            'statsd_port': 8125
        }

        datadog.initialize(**options)
        self.statsd = datadog.statsd

    def inc(self, key):
        self.statsd.increment('example_metric.increment', tags=["environment:dev"])
        self.statsd.increment(key, tags=["environment:dev"])

    def flush(self):
        pass
