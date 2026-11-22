import { useEffect } from 'react';
import { wsClient } from '../services/websocket';
import { useAppStore } from '../stores/appStore';
import { useTranscriptStore } from '../stores/transcriptStore';
import { useAnswerStore } from '../stores/answerStore';
import { WebSocketEvent } from '../types';

export function useWebSocket() {
  const setWsConnected = useAppStore((state) => state.setWsConnected);
  const addSegment = useTranscriptStore((state) => state.addSegment);
  const updatePartial = useTranscriptStore((state) => state.updatePartialSegment);
  const appendStream = useAnswerStore((state) => state.appendStream);
  const finishGeneration = useAnswerStore((state) => state.finishGeneration);
  const updateMetrics = useAppStore((state) => state.updateMetrics);

  useEffect(() => {
    wsClient.connect(
      (event: WebSocketEvent) => {
        switch (event.event) {
          case 'transcription_update':
            if (event.data.is_partial) {
              updatePartial(event.data.text);
            } else {
              addSegment({
                id: `seg-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
                text: event.data.text,
                timestamp: event.data.timestamp_ms || Date.now(),
                isQuestion: event.data.text.includes('?'),
              });
            }
            break;
          case 'answer_stream':
            if (event.data.chunk) {
              appendStream(event.data.chunk);
            }
            if (event.data.done && event.data.answer) {
              finishGeneration(event.data.answer);
            }
            break;
          case 'status_update':
            if (event.data.metrics) {
              updateMetrics(event.data.metrics);
            }
            break;
          default:
            break;
        }
      },
      (connected) => setWsConnected(connected)
    );

    return () => {
      wsClient.disconnect();
    };
  }, [setWsConnected, addSegment, updatePartial, appendStream, finishGeneration, updateMetrics]);
}
