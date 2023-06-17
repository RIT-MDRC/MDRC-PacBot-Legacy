use crate::model::serial_messages::SerialMessageCode;
use crate::service::serial_manager::SerialManager;

mod model;
mod service;

fn main() {
    println!("Hello, world!");

    log4rs::init_file("log4rs.yml", Default::default()).unwrap();

    let mut serial_manager = SerialManager::new();
    // let x = serial_manager.send_message(SerialMessageCode::Repeat, vec![2]);
    serial_manager.connect().unwrap();

    // serial_manager.benchmark(1);
    let mut led_on = false;
    loop {
        // wait for user input
        let mut input = String::new();
        std::io::stdin().read_line(&mut input).unwrap();

        led_on = !led_on;
        serial_manager.send_message(SerialMessageCode::Led, &[led_on as u8]);
    }
    // for i in 0..20 {
    //     let bytes = serial_manager.send_message(SerialMessageCode::Repeat, vec![i + 1]);
    //     // serial_manager.send_byte(i).unwrap();
    //     // serial_manager.flush().unwrap();
    //     // let mut b = serial_manager.receive_byte().unwrap();
    //     // while b != i {
    //     //     b = serial_manager.receive_byte().unwrap();
    //     // }
    //     info!("{:?}", bytes);
    // }

    // println!("{:?}", x);
}
