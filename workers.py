


import asyncio
import time

from backend.queue_manager import event_queue
from backend.metrics import metrics


async def process_event(event):

    start = time.perf_counter()

    revenue = event["price"] * event["quantity"]
    category = event["category"]

    processing_time = (time.perf_counter() - start) * 1000

    async with metrics.lock:

        metrics.events_processed += 1
        metrics.revenue += revenue

        metrics.revenue_by_category.setdefault(category, 0)
        metrics.revenue_by_category[category] += revenue

        metrics.avg_processing_latency = (
            metrics.avg_processing_latency * 0.9
            + processing_time * 0.1
        )


async def worker(worker_id):

    while True:

        event = await event_queue.get()

        await process_event(event)

        event_queue.task_done()


async def start_workers(count):

    tasks = []

    metrics.worker_count = count

    for i in range(count):

        tasks.append(asyncio.create_task(worker(i)))

    return tasks