/// This file is shared between the Arduino and pacbot_services
pub const MAX_SERIAL_MESSAGE_ARGS: usize = 6;

#[derive(Debug)]
pub enum SerialError {
    Unknown,
    UnexpectedMessageArgsCount,
    InvalidMessageCode,
}

#[derive(Clone, Copy)]
pub struct SerialMessage {
    pub id: u8,
    pub message_code: SerialMessageCode,
    pub args: [u8; MAX_SERIAL_MESSAGE_ARGS],
}

#[derive(Clone, Copy)]
#[repr(u8)]
pub enum SerialMessageCode {
    // leave 0 as noop
    Ping = 1,
    Repeat = 2,

    // below are only sent from Arduino to pacbot_services
    MissedMessage = 3,
}

impl SerialMessageCode {
    pub fn send_args_count(&self) -> usize {
        match self {
            Self::Ping => 0,
            Self::Repeat => 1, // repeat argument 1

            Self::MissedMessage => 0,
        }
    }

    pub fn response_args_count(&self) -> usize {
        match self {
            Self::Ping => 0,
            Self::Repeat => 1,

            Self::MissedMessage => 2, // (expected id, actual id)
        }
    }
}

impl TryFrom<u8> for SerialMessageCode {
    type Error = SerialError;

    fn try_from(item: u8) -> Result<Self, SerialError> {
        match item {
            1 => Ok(Self::Ping),
            2 => Ok(Self::Repeat),

            3 => Ok(Self::MissedMessage),

            _ => Err(SerialError::InvalidMessageCode),
        }
    }
}

impl From<SerialMessageCode> for u8 {
    fn from(item: SerialMessageCode) -> Self {
        item as u8
    }
}
