use log::{error, info, trace, warn};
use simple_websockets::Message::Text;
use simple_websockets::{Event, EventHub, Message, Responder};
use std::collections::HashMap;

use crate::model::websocket_messages::*;

#[derive(Debug)]
pub enum WebsocketError {
    ServerLaunch,
    InvalidMessageError,
    ClientClosedError,
}

/// keeps track of the websocket server and active clients
pub struct WebsocketManager {
    /// source of incoming events
    event_hub: EventHub,
    /// map between client ids and the client's `Responder`
    clients: HashMap<u64, Responder>,
}

impl WebsocketManager {
    /// creates a new `WebsocketManager` and launches the server
    pub fn new() -> Result<Self, (WebsocketError, String)> {
        // listen for WebSockets on port 8080:
        let event_hub = simple_websockets::launch(WEBSOCKET_SERVER_PORT);
        match event_hub {
            Ok(event_hub) => {
                let clients: HashMap<u64, Responder> = HashMap::new();
                info!("websocket server started on port {}", WEBSOCKET_SERVER_PORT);
                Ok(Self { event_hub, clients })
            }
            Err(_) => Err((WebsocketError::ServerLaunch, "".to_string())),
        }
    }

    /// run the main loop of the `WebsocketManager`
    pub fn forever(&mut self) {
        loop {
            match self.event_hub.poll_event() {
                Event::Connect(client_id, responder) => {
                    info!("A client connected with id #{}", client_id);
                    // add their Responder to our `clients` map:
                    self.clients.insert(client_id, responder);
                    if self
                        .send_message(
                            client_id,
                            &WebsocketMessage::Ping {
                                data: client_id as u32,
                            },
                        )
                        .is_err()
                    {
                        error!("Error sending welcome ping to new client {}", client_id);
                    }
                }
                Event::Disconnect(client_id) => {
                    warn!("Client #{} disconnected.", client_id);
                    // remove the disconnected client from the clients map:
                    self.clients.remove(&client_id);
                }
                Event::Message(client_id, message) => {
                    match message {
                        Text(t) => {
                            // decode the message into a WebsocketMessage
                            match serde_json::from_str(&t) {
                                Ok(message) => {
                                    info!(
                                        "Received a message from client #{}: {:?}",
                                        client_id, message
                                    );

                                    match self.proc_msg(client_id, message) {
                                        Ok(()) => {}
                                        Err(_) => {
                                            error!("error responding to message")
                                        }
                                    }
                                }
                                Err(e) => {
                                    error!("error interpreting incoming message: {:?}", e);
                                }
                            }
                        }
                        Message::Binary(_) => {
                            error!("received binary message???")
                        }
                    }
                }
            }
        }
    }

    /// process a message from a client
    fn proc_msg(
        &mut self,
        client_id: u64,
        message: WebsocketMessage,
    ) -> Result<(), (WebsocketError, String)> {
        let response = match message {
            WebsocketMessage::Ping { data } => Some(WebsocketMessage::Pong { data }),
            WebsocketMessage::Pong { .. } => None,
        };

        if let Some(response) = response {
            self.send_message(client_id, &response)?;
        }

        Ok(())
    }

    /// try to send a message to a client
    pub fn send_message(
        &mut self,
        client_id: u64,
        message: &WebsocketMessage,
    ) -> Result<(), (WebsocketError, String)> {
        let responder = self.clients.get(&client_id).unwrap();

        let response_str = serde_json::to_string(message);
        match response_str {
            Ok(response_str) => {
                if responder.send(Text(response_str)) {
                    trace!("Sent client {} message: {:?}", client_id, message);
                    Ok(())
                } else {
                    error!("Error sending message, client {} closed", client_id);
                    Err((WebsocketError::ClientClosedError, "".to_string()))
                }
            }
            Err(e) => {
                error!("Error sending message");
                error!("{:?}", message);
                error!("{:?}", e);
                Err((WebsocketError::InvalidMessageError, e.to_string()))
            }
        }
    }

    /// blast a message to all active clients
    pub fn blast_message(
        &mut self,
        message: &WebsocketMessage,
    ) -> Result<(), (WebsocketError, String)> {
        let client_ids = self.clients.keys().cloned().collect::<Vec<u64>>();
        trace!("blast to {} clients: {:?}", client_ids.len(), message);
        for client_id in client_ids {
            self.send_message(client_id, message)?;
        }
        Ok(())
    }
}
