#![no_std]
#![no_main]

mod serial_messages;

use arduino_hal::prelude::*;
use panic_halt as _;

use embedded_hal::serial::Read;
use embedded_hal::serial::Write;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut serial = arduino_hal::default_serial!(dp, pins, 115200);

    /*
     * For examples (and inspiration), head to
     *
     *     https://github.com/Rahix/avr-hal/tree/main/examples
     *
     * NOTE: Not all examples were ported to all boards!  There is a good chance though, that code
     * for a different board can be adapted for yours.  The Arduino Uno currently has the most
     * examples available.
     */

    let mut led = pins.d13.into_output();

    loop {
        let b = serial.read_byte();
        serial.write_byte(b);
        serial.flush();
        // ufmt::uwrite!(&mut serial, "{}", 2);
        // led.toggle();
        // arduino_hal::delay_ms(1000);
    }
}
