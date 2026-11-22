import asyncio
import logging
from app.transcripts.manager import transcript_manager
from app.api.websocket import connection_manager
from app.config import settings
from app.agents.question_detector import question_detector

logger = logging.getLogger("ai_voice_copilot.integrations.grpc")

async def start_grpc_listener():
    """
    Connects to the Rust audio engine gRPC server (AudioService).
    Streams incoming real-time transcription events and pushes them to connected WebSockets.
    Includes exponential backoff and non-blocking retry so Python backend can run standalone.
    """
    target = f"{settings.grpc_host}:{settings.grpc_port}"
    logger.info(f"Targeting Rust STT gRPC stream on {target}...")

    backoff = 2
    max_backoff = 15

    while True:
        channel = None
        try:
            import grpc
            # Import generated proto stubs if available
            try:
                from proto import audio_service_pb2, audio_service_pb2_grpc
                has_stubs = True
            except ImportError:
                has_stubs = False

            if not has_stubs:
                logger.debug("gRPC proto stubs not yet compiled. Running listener in standby mode.")
                await asyncio.sleep(backoff)
                continue

            channel = grpc.aio.insecure_channel(target)
            stub = audio_service_pb2_grpc.AudioServiceStub(channel)

            logger.info(f"Connected to Rust STT gRPC service at {target}. Listening for transcription stream...")
            request = audio_service_pb2.Empty()

            async for event in stub.StreamTranscriptions(request):
                # Reset backoff on successful message
                backoff = 2

                text = event.text.strip()
                if not text:
                    continue

                is_partial = event.is_partial
                # Add to transcript history
                entry = transcript_manager.add_segment(
                    text=text,
                    is_partial=is_partial,
                    timestamp=event.timestamp_ms
                )

                # Broadcast to desktop UI via WebSocket
                if entry:
                    await connection_manager.broadcast("transcript_segment", entry)

                # Check if interviewer asked a question
                if not is_partial:
                    detection = await question_detector.run(text)
                    if detection["is_question"]:
                        await connection_manager.broadcast("question_detected", {
                            "question": detection["detected_question"],
                            "confidence": detection["confidence"],
                        })

        except asyncio.CancelledError:
            logger.info("gRPC listener task cancelled.")
            break
        except Exception as e:
            logger.debug(f"gRPC stream connection attempt to {target}: {e}. Retrying in {backoff}s...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 1.5, max_backoff)
        finally:
            if channel is not None:
                await channel.close()
