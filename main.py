


from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
from pathlib import Path

from backend.event_generator import event_producer
from backend.workers import start_workers
from backend.websocket_manager import manager, metrics_stream
from backend.config import WORKER_COUNT
from backend.calculate_event_generation import calculate_event_rate

app = FastAPI()

frontend_path = Path(__file__).resolve().parent.parent / "frontend"

# Serve static files
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
async def serve_dashboard():
    return FileResponse(frontend_path / "index.html")


@app.on_event("startup")
async def startup():

    asyncio.create_task(event_producer())

    await start_workers(WORKER_COUNT)

    asyncio.create_task(metrics_stream())

    asyncio.create_task(calculate_event_rate())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except:
        manager.disconnect(websocket)