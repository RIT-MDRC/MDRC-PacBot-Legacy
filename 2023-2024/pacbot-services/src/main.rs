use crate::model::serial_messages::SerialMessageCode;
use crate::model::websocket_messages::WebsocketMessage;
use crate::service::serial_manager::SerialManager;
use crate::service::service_controller::{
    ServiceController, ServiceControllerInterface, ServiceMessengers,
};
use crate::service::test_service::{
    TestService, TestServiceInitializationInput, TestServiceInput, TestServiceOutput,
};
use crate::service::websocket_manager::WebsocketManager;
use log::info;
use std::sync::mpsc::channel;
use std::thread;
use std::thread::{sleep, JoinHandle};
use std::time::Duration;

// extern crate simple-websockets;

mod model;
mod service;

fn main() {
    log4rs::init_file("log4rs.yml", Default::default()).unwrap();

    info!("hello world!");

    begin_services();
}

fn begin_services() {
    let _ = start_test_service();

    let mut websocket_manager = WebsocketManager::new().unwrap();
    websocket_manager
        .blast_message(&WebsocketMessage::Ping { data: 100 })
        .unwrap();
    websocket_manager.forever();
}

fn start_test_service() -> (
    ServiceControllerInterface<TestServiceInitializationInput, TestServiceInput, TestServiceOutput>,
    JoinHandle<()>,
) {
    let (initialization_input_sender, initialization_input_receiver) = channel();
    let (input_sender, input_receiver) = channel();
    let (output_sender, output_receiver) = channel();
    let (service_message_sender, service_message_receiver) = channel();
    let (options_sender, options_receiver) = channel();
    let (options_recv_sender, options_recv_receiver) = channel();
    let (debug_sender, debug_receiver) = channel();

    let service_controller_thread = thread::spawn(move || {
        let mut service_controller = ServiceController::new(
            TestService::new(),
            initialization_input_receiver,
            input_receiver,
            output_sender,
            ServiceMessengers {
                service_message_receiver,
                options_receiver,
                options_sender: options_recv_sender,
                debug_sender,
            },
        );

        service_controller.loop_forever();
    });

    let service_controller_interface = ServiceControllerInterface {
        initialization_input_sender,
        input_sender,
        output_receiver,
        service_message_sender,
        options_sender,
        options_receiver: options_recv_receiver,
        debug_receiver,
    };

    sleep(Duration::from_millis(100));

    (service_controller_interface, service_controller_thread)
}
