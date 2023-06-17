use crate::model::serial_messages::*;
use log::{error, trace};
use serialport::SerialPort;
use std::error::Error;
use std::io::{Read, Write};
use std::time::Duration;

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

        match ports {
            Err(e) => Err((SerialError::ErrorListingSerialPorts, e.to_string())),
            Ok(ports) => {
                if ports.is_empty() {
                    return Err((SerialError::NoAvailablePorts, "".to_string()));
                }

                let port_name = ports[0].clone().port_name;

                match serialport::new(port_name, 115_200)
                    .timeout(Duration::from_millis(10))
                    .open()
                {
                    Err(e) => Err((SerialError::ConnectionError, e.to_string())),
                    Ok(p) => {
                        self.serial_port = Some(p);
                        Ok(())
                    }
                }
            }
        }
    }

    pub fn send_byte(&mut self, byte: u8) -> Result<usize, (SerialError, String)> {
        match &mut self.serial_port {
            None => Err((SerialError::NoActiveConnection, "".to_string())),
            Some(port) => match port.write(&[byte]) {
                Err(e) => Err((SerialError::WriteError, e.to_string())),
                Ok(sent) => Ok(sent),
            },
        }
    }

    pub fn receive_byte(&mut self) -> Result<u8, (SerialError, String)> {
        match &mut self.serial_port {
            None => Err((SerialError::NoActiveConnection, "".to_string())),
            Some(port) => {
                let mut bytes = [0];
                match port.read_exact(&mut bytes) {
                    Err(e) => Err((SerialError::ReadError, e.to_string())),
                    Ok(()) => Ok(bytes[0]),
                }
            }
        }
    }

    pub fn flush(&mut self) -> Result<(), (SerialError, String)> {
        match &mut self.serial_port {
            None => Err((SerialError::NoActiveConnection, "".to_string())),
            Some(port) => match port.flush() {
                Ok(()) => Ok(()),
                Err(e) => Err((SerialError::WriteError, e.to_string())),
            },
        }
    }

    fn try_send_message(
        &mut self,
        message_code: SerialMessageCode,
        args: Vec<u8>,
    ) -> Result<[u8; MAX_SERIAL_MESSAGE_ARGS], (SerialError, String)> {
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
            255 => 0,
            x => x + 1,
        };

        // first send the message id
        self.send_byte(message_code.into())?;

        // then send the arguments
        for i in message.args.iter().take(message_code.send_args_count()) {
            self.send_byte(*i)?;
        }

        // receive the response message code
        let response_message_code_u8 = self.receive_byte()?;
        match SerialMessageCode::try_from(response_message_code_u8) {
            Err(e) => Err((e, "".to_string())),
            Ok(response_message_code) => {
                // receive the response arguments
                let mut response_args = [0; MAX_SERIAL_MESSAGE_ARGS];

                for i in response_args
                    .iter_mut()
                    .take(response_message_code.response_args_count())
                {
                    *i = self.receive_byte()?;
                }

                Ok(response_args)
            }
        }
    }

    pub fn send_message(
        &mut self,
        message_code: SerialMessageCode,
        args: Vec<u8>,
    ) -> [u8; MAX_SERIAL_MESSAGE_ARGS] {
        // TODO recover gracefully by clearing buffers and sending 0s
        self.try_send_message(message_code, args).unwrap()
    }
}
