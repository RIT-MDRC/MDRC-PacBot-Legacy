export const WEBSOCKET_SERVER_PORT = 8765;

export type WebsocketMessage = PingMessage | PongMessage;

export interface PingMessage {
    "Ping": {
        "data": number
    }
}

export interface PongMessage {
    "Pong": {
        "data": number
    }
}