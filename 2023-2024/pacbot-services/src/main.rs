use crate::model::serial_messages::SerialMessageCode;
use crate::service::serial_manager::SerialManager;

mod model;
mod service;

fn main() {
    println!("Hello, world!");

    log4rs::init_file("log4rs.yml", Default::default()).unwrap();

    let mut serial_manager = SerialManager::new();
    let x = serial_manager.send_message(SerialMessageCode::Repeat, vec![2]);

    println!("{:?}", x);
}
