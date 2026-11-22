from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json
import logging
import asyncio

from app.transcripts.manager import transcript_manager
from app.orchestration.engine import orchestrator
from app.routing.strategy import AnswerMode

logger = logging.getLogger("ai_voice_copilot.websocket")
router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, event: str, data: Any):
        message = json.dumps({
            "event": event,
            "data": data,
            "timestamp": int(__import__("time").time() * 1000)
        })
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.warning(f"Error broadcasting to client: {e}")
                self.disconnect(connection)

connection_manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            text = await websocket.receive_text()
            try:
                payload = json.loads(text)
                action = payload.get("action")

                if action == "ping":
                    await websocket.send_text(json.dumps({"event": "pong"}))

                elif action == "generate_answer":
                    # Real-time WebSocket streaming of answer
                    question = payload.get("question", "")
                    mode_str = payload.get("mode", "fast")
                    try:
                        mode_enum = AnswerMode(mode_str.lower())
                    except ValueError:
                        mode_enum = AnswerMode.FAST

                    async for stream_event in orchestrator.process_question_stream(question=question, mode=mode_enum):
                        await websocket.send_text(json.dumps({
                            "event": "answer_stream",
                            "data": stream_event
                        }))

                elif action == "add_transcript":
                    # Simulated or injected transcript segment
                    segment_text = payload.get("text", "")
                    is_partial = payload.get("is_partial", False)
                    entry = transcript_manager.add_segment(segment_text, is_partial=is_partial)
                    if entry:
                        await connection_manager.broadcast("transcript_segment", entry)

            except json.JSONDecodeError:
                # Raw text heartbeat
                if text == "ping":
                    await websocket.send_text("pong")
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
    except Exception as e:
        logger.warning(f"WebSocket connection error: {e}")
        connection_manager.disconnect(websocket)
