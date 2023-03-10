from typing import Any, Dict, List, Optional

import datadog

from spoor.exporters.base import Exporter


class DatadogExporter(Exporter):

    _DEFAULT_OPTIONS = {
        "statsd_host": "127.0.0.1",
        "statsd_port": 8125,
    }

    def __init__(
        self,
        *,
        options: Optional[Dict[str, Any]] = None,
        metric: Optional[str] = None,
        group: bool = True,
        extra_tags: Optional[List[str]] = None,
    ):
        self.options = options or self._DEFAULT_OPTIONS
        self.metric = metric
        self.group = group
        self.tags = extra_tags or []
        datadog.initialize(**self.options)
        self.statsd = datadog.statsd

    def send(self, key, **extras):
        metric = self.metric
        if not self.group:
            # NOTE: send each method as a separate metirc
            metric = f"{self.metric}.{key}"
        tags = [f"method:{key}", *self.tags]
        self.statsd.increment(metric=metric, tags=tags)

    def flush(self):
        self.statsd.flush()
