use crate::service::service_controller::{
    ServiceControllerDebug, ServiceControllerOptions, ServiceControllerStatus,
};
use serde::{Deserialize, Serialize};

pub const WEBSOCKET_SERVER_PORT: u16 = 8765;

#[derive(Serialize, Deserialize, Debug)]
pub enum WebsocketMessage {
    Ping { data: u32 },
    Pong { data: u32 },

    WebsocketMessageFromClient(WebsocketMessageFromClient),
    WebsocketMessageFromServer(WebsocketMessageFromServer),
}

#[derive(Serialize, Deserialize, Debug)]
pub enum WebsocketMessageFromClient {
    GetStatus,
    GetOptions,
    GetDebug(usize),
    GetDefaultInitializationInput,
    GetDefaultInput,
    GetLastOutput,

    Initialize(String),
    SetOptions(usize, ServiceControllerOptions),
    SendInput(String),
    Step,
    Uninitialize,
}

#[derive(Serialize, Deserialize, Debug)]
pub enum WebsocketMessageFromServer {
    Status(Vec<(usize, ServiceControllerStatus)>),
    Options(Vec<(usize, ServiceControllerOptions)>),
    Debug((usize, ServiceControllerDebug)),
    DefaultInitializationInput((usize, String)),
    DefaultInput((usize, String)),
    LastOutput((usize, String)),
}
