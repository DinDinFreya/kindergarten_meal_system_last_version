import json
import redis.asyncio as redis
from fastapi import WebSocket, WebSocketDisconnect
from app.config import settings
from app.database import get_db
from app.models.ingredient import Ingredient
from sqlalchemy.orm import Session
from typing import Dict, Set

# Redis client for pub/sub
redis_client = redis.from_url(settings.REDIS_URL)

# Store active WebSocket connections
connected_clients: Set[WebSocket] = set()

async def websocket_endpoint(websocket: WebSocket, db: Session = None):
    # Accept WebSocket connection
    await websocket.accept()
    connected_clients.add(websocket)
    
    try:
        # Subscribe to Redis pub/sub channel for inventory updates
        pubsub = redis_client.pubsub()
        await pubsub.subscribe("inventory_updates")
        
        # Send initial inventory state
        if db is None:
            db = next(get_db())
        inventory = db.query(Ingredient).all()
        low_stock = [
            {"id": item.id, "name": item.name, "quantity": item.quantity}
            for item in inventory if item.quantity <= settings.LOW_STOCK_THRESHOLD
        ]
        await websocket.send_json({
            "type": "initial_state",
            "inventory": [
                {"id": item.id, "name": item.name, "quantity": item.quantity}
                for item in inventory
            ],
            "low_stock_alerts": low_stock
        })
        
        # Listen for Redis messages and forward to client
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await websocket.send_json(data)
                
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
    finally:
        await pubsub.unsubscribe("inventory_updates")
        await pubsub.close()
        connected_clients.remove(websocket)
        if db:
            db.close()

async def broadcast_inventory_update(data: Dict):
    """Broadcast inventory updates to all connected clients via Redis."""
    await redis_client.publish("inventory_updates", json.dumps(data))

async def check_low_stock(db: Session):
    """Check for low stock and broadcast alerts."""
    low_stock_items = db.query(Ingredient).filter(
        Ingredient.quantity <= settings.LOW_STOCK_THRESHOLD
    ).all()
    if low_stock_items:
        alert_data = {
            "type": "low_stock_alert",
            "items": [
                {"id": item.id, "name": item.name, "quantity": item.quantity}
                for item in low_stock_items
            ]
        }
        await broadcast_inventory_update(alert_data)