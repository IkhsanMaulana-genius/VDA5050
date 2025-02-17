import json
from fastapi import FastAPI, WebSocket
from agv_simulator import AGVSimulator
import asyncio

app = FastAPI()
agv = AGVSimulator()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(1)
        state = json.dumps(agv.state)
        await websocket.send_text(state)

@app.on_event("startup")
async def startup_event():
    async def periodic_state_update():
        while True:
            agv.publish_state()
            await asyncio.sleep(2)
    asyncio.create_task(periodic_state_update())