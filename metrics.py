
import asyncio


class Metrics:

    def __init__(self):

        self.lock = asyncio.Lock()

        # event stats
        self.events_generated = 0
        self.events_processed = 0
        self.events_per_sec = 0

        # revenue
        self.revenue = 0
        self.revenue_by_category = {}

        # system stats
        self.queue_backlog = 0
        self.clients = 0
        self.worker_count = 0

        # latency
        self.avg_processing_latency = 0
        self.websocket_latency = 0


metrics = Metrics()