import { WebSocketEvent } from '../types';

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private onMessageCallback: ((event: WebSocketEvent) => void) | null = null;
  private onStatusCallback: ((connected: boolean) => void) | null = null;
  private reconnectInterval = 3000;
  private shouldReconnect = true;

  constructor(url: string = 'ws://127.0.0.1:8000/ws') {
    this.url = url;
  }

  public connect(
    onMessage: (event: WebSocketEvent) => void,
    onStatus: (connected: boolean) => void
  ) {
    this.onMessageCallback = onMessage;
    this.onStatusCallback = onStatus;
    this.shouldReconnect = true;
    this.initSocket();
  }

  private initSocket() {
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.onStatusCallback?.(true);
      };

      this.ws.onmessage = (event) => {
        try {
          const parsed: WebSocketEvent = JSON.parse(event.data);
          this.onMessageCallback?.(parsed);
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };

      this.ws.onclose = () => {
        this.onStatusCallback?.(false);
        if (this.shouldReconnect) {
          setTimeout(() => this.initSocket(), this.reconnectInterval);
        }
      };

      this.ws.onerror = (err) => {
        console.error('WebSocket error:', err);
        this.ws?.close();
      };
    } catch (err) {
      this.onStatusCallback?.(false);
      if (this.shouldReconnect) {
        setTimeout(() => this.initSocket(), this.reconnectInterval);
      }
    }
  }

  public send(event: string, data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ event, data, timestamp: Date.now() }));
    }
  }

  public disconnect() {
    this.shouldReconnect = false;
    this.ws?.close();
    this.ws = null;
  }
}

export const wsClient = new WebSocketClient();
