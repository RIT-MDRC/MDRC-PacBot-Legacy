use crate::model::serial_messages::*;
use log::{debug, error, info, trace, warn};
use serialport::{ClearBuffer, SerialPort};
use std::io::{Read, Write};
use std::time::{Duration, Instant};

const MAX_BYTE_VALUE: u8 = 254;

pub struct SerialManager {
    next_message_id: u8,
    sent_messages: [SerialMessage; 255],
    serial_port: Option<Box<dyn SerialPort>>,
}

impl SerialManager {
    pub fn new() -> Self {
        Self {
            next_message_id: 0,
            sent_messages: [SerialMessage {
                id: 0,
                message_code: SerialMessageCode::Ping,
                args: [0; MAX_SERIAL_MESSAGE_ARGS],
            }; 255],
            serial_port: None,
        }
    }

    pub fn connect(&mut self) -> Result<(), (SerialError, String)> {
        let ports = serialport::available_ports();
        info!("ports: {:?}", ports);

        match ports {
            Err(e) => Err((SerialError::ErrorListingSerialPorts, e.to_string())),
            Ok(ports) => {
                if ports.is_empty() {
                    error!("no available ports");
                    return Err((SerialError::NoAvailablePorts, "".to_string()));
                }

                let port_name = ports[0].clone().port_name;
                info!("connecting to first available port: {:?}", port_name);

                match serialport::new(port_name, BAUD_RATE)
                    .timeout(Duration::from_secs(10))
                    .open()
                {
                    Err(e) => {
                        error!("error connecting to port: {}", e.to_string());
                        Err((SerialError::ConnectionError, e.to_string()))
                    }
                    Ok(p) => {
                        info!("connected, clearing buffers...");
                        match p.clear(ClearBuffer::All) {
                            Err(e) => {
                                error!("error clearing buffers: {}", e.to_string());
                                Err((SerialError::ReadError, e.to_string()))
                            }
                            Ok(()) => {
                                self.serial_port = Some(p);
                                info!("buffers cleared, doing ping test...");
                                self.try_send_message(SerialMessageCode::Ping, &[])?;
                                info!("connection successful");
                                Ok(())
                            }
                        }
                    }
                }
            }
        }
    }

    pub fn send_byte(&mut self, byte: u8) -> Result<usize, (SerialError, String)> {
        match &mut self.serial_port {
            None => {
                warn!("tried to write to serial port before connecting");
                Err((SerialError::NoActiveConnection, "".to_string()))
            }
            Some(port) => match port.write(&[byte]) {
                Err(e) => {
                    trace!("error sending {}: {}", byte, e.to_string());
                    Err((SerialError::WriteError, e.to_string()))
                }
                Ok(sent) => {
                    trace!("sent {}", byte);
                    Ok(sent)
                }
            },
        }
    }

    pub fn receive_byte(&mut self) -> Result<u8, (SerialError, String)> {
        match &mut self.serial_port {
            None => {
                warn!("tried to write to serial port before connecting");
                Err((SerialError::NoActiveConnection, "".to_string()))
            }
            Some(port) => {
                let mut bytes = [0];
                match port.read_exact(&mut bytes) {
                    Err(e) => {
                        trace!("read error: {}", e.to_string());
                        Err((SerialError::ReadError, e.to_string()))
                    }
                    Ok(()) => {
                        trace!("read {}", bytes[0]);
                        Ok(bytes[0])
                    }
                }
            }
        }
    }

    pub fn flush(&mut self) -> Result<(), (SerialError, String)> {
        match &mut self.serial_port {
            None => Err((SerialError::NoActiveConnection, "".to_string())),
            Some(port) => match port.flush() {
                Ok(()) => {
                    trace!("flush ok");
                    Ok(())
                }
                Err(e) => {
                    trace!("flush error: {}", e.to_string());
                    Err((SerialError::WriteError, e.to_string()))
                }
            },
        }
    }

    fn try_send_message(
        &mut self,
        message_code: SerialMessageCode,
        args: &[u8],
    ) -> Result<Vec<u8>, (SerialError, String)> {
        if message_code.send_args_count() != args.len() {
            error!(
                "skipping message {} expected args count: {}, received args count {}",
                message_code as u8,
                message_code.send_args_count(),
                args.len()
            );

            return Err((SerialError::UnexpectedMessageArgsCount, "".to_string()));
        }

        let mut message_args = [0; MAX_SERIAL_MESSAGE_ARGS];

        message_args[..message_code.send_args_count()]
            .copy_from_slice(&args[..message_code.send_args_count()]);

        self.sent_messages[self.next_message_id as usize] = SerialMessage {
            id: self.next_message_id,
            message_code,
            args: message_args,
        };

        let message = self.sent_messages[self.next_message_id as usize];

        self.next_message_id = match self.next_message_id {
            MAX_BYTE_VALUE => 0,
            x => x + 1,
        };

        debug!("sending message id {}", message.id);
        self.send_byte(message.id)?;

        debug!("sending message code {:?}", message_code);
        self.send_byte(message_code.into())?;

        debug!("sending args {:?}", args);
        // then send the arguments
        for i in message.args.iter().take(message_code.send_args_count()) {
            self.send_byte(*i)?;
        }

        self.flush()?;

        info!(
            "sent full message with id: {}; code: '{:?}'; args: {:?}",
            message.id, message_code, args
        );

        // receive the message id
        let received_message_id = self.receive_byte()?;
        debug!("receive message id {}", received_message_id);
        // receive the response message code
        let response_message_code_u8 = self.receive_byte()?;
        debug!("receive message code {}", response_message_code_u8);
        match SerialMessageCode::try_from(response_message_code_u8) {
            Err(e) => Err((e, "".to_string())),
            Ok(response_message_code) => {
                debug!("message code = {:?}", response_message_code);
                // receive the response arguments
                let mut response_args = Vec::new();

                #[allow(clippy::needless_range_loop)]
                for _ in 0..response_message_code.response_args_count() {
                    response_args.push(self.receive_byte()?);
                }

                info!(
                    "receive message with id: {}; code: '{:?}'; args: {:?}",
                    received_message_id, response_message_code, response_args
                );

                Ok(response_args)
            }
        }
    }

    #[allow(dead_code)]
    pub fn benchmark(&mut self, seconds: u64) -> i32 {
        warn!("running serial port benchmark");
        match &mut self.serial_port {
            None => {
                error!("attempted to benchmark without a connection");
                0
            }
            Some(_) => {
                let start_time = Instant::now();
                let mut ping_count = 0;
                let args = [0; MAX_SERIAL_MESSAGE_ARGS].to_vec();
                while start_time.elapsed() < Duration::from_secs(seconds) {
                    match self.try_send_message(SerialMessageCode::RepeatMax, &args) {
                        Err((e, msg)) => {
                            error!("Encountered error {:?} during ping: {}", e, msg);
                            return ping_count;
                        }
                        Ok(_) => {
                            ping_count += 1;
                        }
                    }
                }
                warn!(
                    "finished benchmark with score of {}, or {} bits",
                    ping_count,
                    (MAX_SERIAL_MESSAGE_ARGS + 2) * 2 * 8 * (ping_count as usize)
                );
                ping_count
            }
        }
    }

    pub fn send_message(&mut self, message_code: SerialMessageCode, args: &[u8]) -> Vec<u8> {
        // TODO recover gracefully by clearing buffers and sending 0s
        self.try_send_message(message_code, args).unwrap()
    }
}
