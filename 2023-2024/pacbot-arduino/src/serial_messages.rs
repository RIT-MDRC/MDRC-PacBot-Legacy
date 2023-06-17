/// This file is shared between the Arduino and pacbot_services

/// the maximum number of arguments for any given message
///
/// anything above 12 here starts to take a performance hit to messages/s
/// note that at current max efficiency the pipe is about half empty because synchronous messages
/// mean that one arduino waits to receive the whole request before sending the response, and vice
/// versa on the other side
/// this could be enhanced in the future, but it would require more complex processing logic
pub const MAX_SERIAL_MESSAGE_ARGS: usize = 12;
/// baud rate for serial communication, measured in bits/s both ways
pub const BAUD_RATE: u32 = 115200;

/// defines the types of errors that the serial communication may encounter
#[derive(Debug)]
pub enum SerialError {
    Unknown,
    /// the number of arguments given does not match the defined number of arguments for
    /// the given message code
    UnexpectedMessageArgsCount,
    /// the message code does not exist
    InvalidMessageCode,
    /// no serial ports were found
    NoAvailablePorts,
    /// there was an error listing available serial ports
    ErrorListingSerialPorts,
    /// encountered an error while trying to connect to the serial port
    ConnectionError,
    /// tried to carry out an action before connecting to a serial port
    NoActiveConnection,
    /// encountered an error writing to the serial port
    WriteError,
    /// encountered an error reading from the serial port
    ReadError,
}

/// the parts needed to send a message over the serial port
#[derive(Clone, Copy)]
pub struct SerialMessage {
    /// incrementing identifier, used to tell if a message has been skipped
    pub id: u8,
    /// the type of the message
    pub message_code: SerialMessageCode,
    /// the arguments for the message
    pub args: [u8; MAX_SERIAL_MESSAGE_ARGS],
}

/// the possible types for messages
///
/// leave 0 as undefined/noop
#[derive(Clone, Copy, Debug)]
#[repr(u8)]
pub enum SerialMessageCode {
    /// no arguments, just send ping back
    Ping = 1,
    /// one argument, repeat the argument back
    Repeat = 2,
    /// [MAX_SERIAL_MESSAGE_ARGS] arguments, repeat them all back
    RepeatMax = 4,
    /// one argument, set the led low (0) or high (1)
    Led = 5,

    /// one argument representing the sensor to fetch
    DistanceSingle = 6,
    /// four arguments representing the sensors to fetch
    ///
    /// each distance sensor produces a 16-bit output
    DistanceQuadruple = 7,

    /// four arguments, one for each motor speed
    ///
    /// assume each encoder output fits in 3 bytes?
    MotorsEncoders = 8,

    /// sent from arduino to pacbot_services if arduino identifies that a message was skipped
    MissedMessage = 3,
}

impl SerialMessageCode {
    /// get the number of arguments associated with sending a given message
    pub fn send_args_count(&self) -> usize {
        match self {
            Self::Ping => 0,
            Self::Repeat => 1, // repeat argument 1
            Self::RepeatMax => MAX_SERIAL_MESSAGE_ARGS,
            Self::Led => 1,

            Self::DistanceSingle => 1,
            Self::DistanceQuadruple => 4,

            // one for each motor speed
            Self::MotorsEncoders => 4,

            Self::MissedMessage => 0,
        }
    }

    /// get the number of arguments associated with receiving a given message
    pub fn response_args_count(&self) -> usize {
        match self {
            Self::Ping => 0,
            Self::Repeat => 1,
            Self::RepeatMax => MAX_SERIAL_MESSAGE_ARGS,
            Self::Led => 0,

            Self::DistanceSingle => 2,
            Self::DistanceQuadruple => 8,

            Self::MotorsEncoders => 4,

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
            4 => Ok(Self::RepeatMax),
            5 => Ok(Self::Led),

            6 => Ok(Self::DistanceSingle),
            7 => Ok(Self::DistanceQuadruple),

            8 => Ok(Self::MotorsEncoders),

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
