from fastapi import WebSocket
import asyncio
import time

from metrics import metrics
from queue_manager import event_queue
from config import WEBSOCKET_CLIENT_LIMIT, METRIC_UPDATE_INTERVAL

class ConnectionManager:

    def __init__(self):
        self.clients = []

    async def connect(self, websocket: WebSocket):

        if len(self.clients) >= WEBSOCKET_CLIENT_LIMIT:
            await websocket.close()
            return

        await websocket.accept()

        self.clients.append(websocket)

        metrics.clients = len(self.clients)

    def disconnect(self, websocket):

        if websocket in self.clients:
            self.clients.remove(websocket)

        metrics.clients = len(self.clients)

    async def broadcast(self, data):

        start = time.time()

        disconnected_clients = []

        for client in list(self.clients):

            try:
                await client.send_json(data)

            except:
                disconnected_clients.append(client)

        for client in disconnected_clients:
            self.disconnect(client)

        metrics.websocket_latency = (time.time() - start) * 1000


manager = ConnectionManager()


async def metrics_stream():

    while True:

        data = {
            "events_generated": metrics.events_generated,
            "events_processed": metrics.events_processed,
            "events_per_sec": metrics.events_per_sec,

            "queue_backlog": event_queue.qsize(),

            "revenue": metrics.revenue,
            "revenue_by_category": metrics.revenue_by_category,

            "clients": metrics.clients,
            "workers": metrics.worker_count,

            "avg_processing_latency": metrics.avg_processing_latency,
            "websocket_latency": metrics.websocket_latency
        }

        await manager.broadcast(data)

        await asyncio.sleep(METRIC_UPDATE_INTERVAL)