from typing import Optional

import statsd

from spoor.exporters.base import Exporter


class StatsdExporter(Exporter):
    def __init__(
        self,
        *,
        metric: Optional[str] = None,
        options,
    ):
        # TODO: use default options if not provided
        self.metric = metric
        self.statsd = statsd.StatsClient(
            host=options["statsd_host"],
            port=options["statsd_port"],
            prefix=self.metric,
        )

    def send(self, key, **extras):
        self.statsd.incr(key)

    def flush(self):
        self.statsd.close()
