#![no_std]
#![no_main]

mod serial_messages;

use panic_halt as _;

use crate::serial_messages::*;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut serial = arduino_hal::default_serial!(dp, pins, BAUD_RATE);

    let mut led = pins.d13.into_output();

    loop {
        let message_id = serial.read_byte();
        let message_code = serial.read_byte();

        match SerialMessageCode::try_from(message_code) {
            Err(_) => continue,
            Ok(code) => {
                let mut args = [0; MAX_SERIAL_MESSAGE_ARGS];

                #[allow(clippy::needless_range_loop)]
                for i in 0..code.send_args_count() {
                    args[i] = serial.read_byte();
                }

                let response = match code {
                    SerialMessageCode::Ping => msg_noop(&args),
                    SerialMessageCode::Repeat => msg_repeat(&args),
                    SerialMessageCode::RepeatMax => msg_repeat(&args),
                    SerialMessageCode::Led => {
                        match args[0] {
                            0 => led.set_low(),
                            _ => led.set_high()
                        }

                        &args
                    }

                    SerialMessageCode::DistanceSingle => msg_noop(&args),
                    SerialMessageCode::DistanceQuadruple => msg_noop(&args),

                    SerialMessageCode::MotorsEncoders => msg_noop(&args),

                    SerialMessageCode::MissedMessage => msg_noop(&args),
                };

                serial.write_byte(message_id);
                serial.write_byte(message_code);

                #[allow(clippy::needless_range_loop)]
                for i in 0..code.response_args_count() {
                    serial.write_byte(response[i]);
                }
                serial.flush();
            }
        }
    }
}

fn msg_noop(_args: &[u8; MAX_SERIAL_MESSAGE_ARGS]) -> &[u8; MAX_SERIAL_MESSAGE_ARGS] {
    &[0; MAX_SERIAL_MESSAGE_ARGS]
}

fn msg_repeat(args: &[u8; MAX_SERIAL_MESSAGE_ARGS]) -> &[u8; MAX_SERIAL_MESSAGE_ARGS] {
    args
}