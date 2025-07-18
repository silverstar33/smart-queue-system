from fastapi import WebSocket
from typing import List
import json

clients: List[WebSocket] = []

async def register_client(client: WebSocket):
    await client.accept()
    clients.append(client)

def remove_client(client: WebSocket):
    if client in clients:
        clients.remove(client)

async def broadcast_update(message: dict):
    for client in clients:
        try:
            await client.send_text(json.dumps(message))
        except:
            remove_client(client)
