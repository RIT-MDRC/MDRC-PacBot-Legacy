import { onMount } from 'svelte';

class WebSocketClient {
    private socket: WebSocket | null = null;
    private url: string | null = null;

    constructor() { }

    setUrl(url: string) {
        this.url = url
    }

    connect(): Promise<Event> {
        return new Promise((resolve, reject) => {
            if (this.url == null) {
                console.error('no url set!');
                return;
            }
            this.socket = new WebSocket(this.url);

            this.socket.onopen = (event: Event) => {
                console.log('WebSocket is open now.');
                resolve(event);
            };

            this.socket.onclose = (event: CloseEvent) => {
                console.log('WebSocket is closed now.', event);
            };

            this.socket.onerror = (event: Event) => {
                console.error('WebSocket encountered error: ', event);
                reject(event);
            };

            this.socket.onmessage = (event: MessageEvent) => {
                console.log('WebSocket message received: ', event);
            };
        });
    }

    sendMessage(msg: string): void {
        if (!this.socket || this.socket.readyState !== this.socket.OPEN) {
            console.error('Socket is not open.');
            return;
        }
        this.socket.send(msg);
    }
}

// connection is done in page.svelte
export let websocketClient: WebSocketClient = new WebSocketClient();
