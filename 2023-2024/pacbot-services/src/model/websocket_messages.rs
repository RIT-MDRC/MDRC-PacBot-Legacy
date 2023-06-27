use serde::{Deserialize, Serialize};

pub const WEBSOCKET_SERVER_PORT: u16 = 8765;

#[derive(Serialize, Deserialize, Debug)]
pub enum WebsocketMessage {
    Ping { data: u32 },
    Pong { data: u32 },
}
