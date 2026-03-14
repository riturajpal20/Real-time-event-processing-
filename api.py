from fastapi import APIRouter
from metrics import metrics
from queue_manager import event_queue

router = APIRouter()


@router.get("/metrics")
async def get_metrics():

    return {
        "events_generated": metrics.events_generated,
        "events_processed": metrics.events_processed,
        "events_per_sec": metrics.events_per_sec,
        "queue_backlog": event_queue.qsize(),
        "revenue": metrics.revenue
    }