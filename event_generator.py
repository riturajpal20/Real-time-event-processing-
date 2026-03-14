

import asyncio
import time
import random
import uuid

from backend.config import EVENT_RATE
from backend.queue_manager import event_queue
from backend.metrics import metrics


categories = ["electronics", "clothing", "home", "sports"]


async def event_producer():

    while True:

        start = time.time()
        events_this_second = 0

        for _ in range(EVENT_RATE):

            event = {
                "event_id": str(uuid.uuid4()),
                "timestamp": time.time(),
                "user_id": random.randint(1, 10000),
                "product_id": random.randint(1, 5000),
                "category": random.choice(categories),
                "price": round(random.uniform(10, 500), 2),
                "quantity": random.randint(1, 5)
            }

            await event_queue.put(event)

            metrics.events_generated += 1
            events_this_second += 1

        metrics.events_per_sec = events_this_second

        elapsed = time.time() - start

        await asyncio.sleep(max(0, 1 - elapsed))