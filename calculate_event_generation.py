import asyncio
from metrics import metrics


async def calculate_event_rate():

    last_count = metrics.events_generated

    while True:

        await asyncio.sleep(1)

        current_count = metrics.events_generated

        metrics.events_per_sec = current_count - last_count

        last_count = current_count