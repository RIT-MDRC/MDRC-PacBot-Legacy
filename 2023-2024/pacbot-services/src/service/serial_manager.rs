use crate::model::serial_messages::*;
use log::{error, trace};

pub struct SerialManager {
    next_message_id: u8,
    sent_messages: [SerialMessage; 255],
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
        }
    }

    fn send_byte(&mut self, byte: u8) -> Result<(), SerialError> {
        // TODO
        trace!("sent: {}", byte);
        Ok(())
    }

    fn receive_byte(&self) -> Result<u8, SerialError> {
        // TODO
        Ok(0)
    }

    fn try_send_message(
        &mut self,
        message_code: SerialMessageCode,
        args: Vec<u8>,
    ) -> Result<[u8; MAX_SERIAL_MESSAGE_ARGS], SerialError> {
        if message_code.send_args_count() != args.len() {
            error!(
                "skipping message {} expected args count: {}, received args count {}",
                message_code as u8,
                message_code.send_args_count(),
                args.len()
            );

            return Err(SerialError::UnexpectedMessageArgsCount);
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
        let response_message_code: SerialMessageCode = self.receive_byte()?.try_into()?;

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

    pub fn send_message(
        &mut self,
        message_code: SerialMessageCode,
        args: Vec<u8>,
    ) -> [u8; MAX_SERIAL_MESSAGE_ARGS] {
        // TODO recover gracefully by clearing buffers and sending 0s
        self.try_send_message(message_code, args).unwrap()
    }
}
