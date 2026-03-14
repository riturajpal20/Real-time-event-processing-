import asyncio
from .config import MAX_QUEUE_SIZE

event_queue = asyncio.Queue(maxsize=MAX_QUEUE_SIZE)


def get_queue_size():
    return event_queue.qsize()