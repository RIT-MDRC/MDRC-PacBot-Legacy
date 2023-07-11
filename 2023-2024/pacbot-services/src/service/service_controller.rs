use log::{error, info, trace};
use serde::{Deserialize, Serialize};
use std::sync::mpsc::{Receiver, Sender};

#[derive(Clone, Serialize, Deserialize)]
pub enum ServiceOption {
    OptionGroup(String, ServiceOptionGroup),
    Button(String, bool),
    Number(String, i32),
    UnsignedNumber(String, u32),
}

#[derive(Clone, Serialize, Deserialize)]
pub struct ServiceOptionGroup {
    pub options: Vec<ServiceOption>,
}

#[derive(Clone, Serialize, Deserialize)]
pub struct ServiceControllerOptions {
    pub paused: bool,

    pub service_options: ServiceOptionGroup,
}

#[derive(Clone, Serialize, Deserialize)]
pub enum ServiceDebugEntry {
    DebugGroup(String, ServiceDebugGroup),
    Int(String, i32),
    Float(String, f32),
    Text(String, String),
}

#[derive(Clone, Serialize, Deserialize)]
pub struct ServiceDebugGroup {
    pub debug: Vec<ServiceDebugEntry>,
}

#[derive(Clone, Serialize, Deserialize)]
pub struct ServiceControllerDebug {
    pub initialized: bool,
    pub new_input_available: bool,

    pub service_debug: ServiceDebugGroup,
}

pub trait Service<S, I, O> {
    fn get_options(&self) -> ServiceOptionGroup;

    fn get_debug(&self) -> ServiceDebugGroup;

    fn get_default_input(&self) -> I;

    fn set_options(&mut self, options: &ServiceOptionGroup);

    fn initialize(&mut self, initialization_values: S) -> Result<(), String>;

    fn step(&mut self, input_values: &I) -> Result<O, String>;

    fn uninitialize(&mut self);
}

#[derive(Serialize, Deserialize)]
pub enum ServiceMessage {
    SendOptions,
    SendDebug,

    Step,

    Uninitialize,
    End,
}

pub struct ServiceMessengers {
    pub service_message_receiver: Receiver<ServiceMessage>,

    pub options_receiver: Receiver<ServiceControllerOptions>,
    pub options_sender: Sender<ServiceControllerOptions>,

    pub debug_sender: Sender<ServiceControllerDebug>,
}

pub struct ServiceController<S, I, O> {
    service: Box<dyn Service<S, I, O>>,
    options: ServiceControllerOptions,
    debug: ServiceControllerDebug,

    initialization_input_receiver: Receiver<S>,

    input_receiver: Receiver<I>,
    output_sender: Sender<O>,

    last_input: Option<I>,

    service_messengers: ServiceMessengers,
}

impl<S, I, O> ServiceController<S, I, O> {
    pub fn new(
        service: impl Service<S, I, O> + 'static,
        initialization_input_receiver: Receiver<S>,
        input_receiver: Receiver<I>,
        output_sender: Sender<O>,
        service_messengers: ServiceMessengers,
    ) -> Self {
        let options = service.get_options();
        let debug = service.get_debug();

        Self {
            service: Box::new(service),
            options: ServiceControllerOptions {
                paused: false,

                service_options: options,
            },
            debug: ServiceControllerDebug {
                initialized: false,
                new_input_available: false,

                service_debug: debug,
            },

            initialization_input_receiver,

            input_receiver,
            output_sender,

            last_input: None,
            service_messengers,
        }
    }

    pub fn loop_forever(&mut self) {
        loop {
            // fetch initialization input
            while let Ok(initialization_values) = self.initialization_input_receiver.try_recv() {
                if !self.debug.initialized {
                    match self.service.initialize(initialization_values) {
                        Ok(()) => {
                            self.debug.initialized = true;
                            info!("initialized service");
                        }
                        Err(e) => {
                            error!("error initializing service: {}", e.to_string());
                        }
                    }
                }
            }
            // fetch options
            while let Ok(options) = self.service_messengers.options_receiver.try_recv() {
                self.service.set_options(&options.service_options);
                self.options = options;
            }
            // fetch input
            while let Ok(input_values) = self.input_receiver.try_recv() {
                self.last_input = Some(input_values);
                if !self.options.paused {
                    self.debug.new_input_available = true;
                }
            }
            // process service messages
            while let Ok(service_message) =
                self.service_messengers.service_message_receiver.try_recv()
            {
                match service_message {
                    ServiceMessage::SendOptions => {
                        match self
                            .service_messengers
                            .options_sender
                            .send(self.options.clone())
                        {
                            Ok(()) => {
                                info!("sent service options")
                            }
                            Err(e) => {
                                error!("error sending service options: {}", e.to_string())
                            }
                        }
                    }
                    ServiceMessage::SendDebug => {
                        self.debug.service_debug = self.service.get_debug();

                        match self
                            .service_messengers
                            .debug_sender
                            .send(self.debug.clone())
                        {
                            Ok(()) => {
                                trace!("sent service debug info")
                            }
                            Err(e) => {
                                error!("error sending service debug: {}", e.to_string())
                            }
                        }
                    }
                    ServiceMessage::Step => {
                        if self.debug.initialized {
                            self.debug.new_input_available = true;
                        }
                    }
                    ServiceMessage::Uninitialize => {
                        if self.debug.initialized {
                            self.service.uninitialize();
                            self.debug.initialized = false;
                        }
                    }
                    ServiceMessage::End => {
                        if self.debug.initialized {
                            self.service.uninitialize();
                            self.debug.initialized = false;
                        }
                        return;
                    }
                }
            }
            // run service
            if self.debug.initialized && self.debug.new_input_available {
                if let Some(input) = &self.last_input {
                    info!("stepping service");
                    match self.service.step(input) {
                        Ok(output) => match self.output_sender.send(output) {
                            Ok(()) => trace!("sent output"),
                            Err(e) => error!("error sending output: {}", e.to_string()),
                        },
                        Err(e) => {
                            error!("error stepping service: {}", e.to_string());
                        }
                    }
                }
                self.debug.new_input_available = false;
            }
        }
    }
}

pub struct ServiceControllerInterface<S, I, O> {
    pub initialization_input_sender: Sender<S>,
    pub input_sender: Sender<I>,
    pub output_receiver: Receiver<O>,
    pub service_message_sender: Sender<ServiceMessage>,
    pub options_sender: Sender<ServiceControllerOptions>,
    pub options_receiver: Receiver<ServiceControllerOptions>,
    pub debug_receiver: Receiver<ServiceControllerDebug>,
}

// tests for service controller
#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::mpsc::channel;
    use std::thread;
    use std::thread::{sleep, JoinHandle};
    use std::time::Duration;
    use test_log::test;

    struct ValueService {
        initial_value: usize,
        value: usize,
    }
    enum ValueServiceInstructions {
        Store(usize),
        ReturnZero,
        ReturnStored,
        ReturnInitial,
        WaitThenReturnZero,
    }
    impl Service<usize, ValueServiceInstructions, usize> for ValueService {
        fn get_options(&self) -> ServiceOptionGroup {
            ServiceOptionGroup { options: vec![] }
        }

        fn get_debug(&self) -> ServiceDebugGroup {
            ServiceDebugGroup { debug: vec![] }
        }

        fn get_default_input(&self) -> ValueServiceInstructions {
            ValueServiceInstructions::Store(0)
        }

        fn set_options(&mut self, _options: &ServiceOptionGroup) {}

        fn initialize(&mut self, initialization_values: usize) -> Result<(), String> {
            self.initial_value = initialization_values;
            self.value = 0;
            Ok(())
        }

        fn step(&mut self, input_values: &ValueServiceInstructions) -> Result<usize, String> {
            match input_values {
                ValueServiceInstructions::Store(x) => {
                    self.value = *x;
                    Ok(self.value)
                }
                ValueServiceInstructions::ReturnZero => Ok(0),
                ValueServiceInstructions::ReturnStored => Ok(self.value),
                ValueServiceInstructions::ReturnInitial => Ok(self.initial_value),
                ValueServiceInstructions::WaitThenReturnZero => {
                    sleep(Duration::from_millis(1000));
                    Ok(0)
                }
            }
        }

        fn uninitialize(&mut self) {
            self.value = 0;
        }
    }

    fn start_value_service() -> (
        ServiceControllerInterface<usize, ValueServiceInstructions, usize>,
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
                ValueService {
                    initial_value: 0,
                    value: 0,
                },
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

    #[test]
    fn test_controller_lifecycle() {
        let (service_controller_interface, service_controller_thread) = start_value_service();

        service_controller_interface
            .initialization_input_sender
            .send(0)
            .unwrap();
        service_controller_interface
            .service_message_sender
            .send(ServiceMessage::SendOptions)
            .unwrap();
        service_controller_interface
            .service_message_sender
            .send(ServiceMessage::SendDebug)
            .unwrap();
        service_controller_interface
            .service_message_sender
            .send(ServiceMessage::Step)
            .unwrap();
        service_controller_interface
            .service_message_sender
            .send(ServiceMessage::Uninitialize)
            .unwrap();
        service_controller_interface
            .service_message_sender
            .send(ServiceMessage::End)
            .unwrap();

        service_controller_thread.join().unwrap();
    }

    #[test]
    fn test_controller_message_send_options() {
        let (interface, _thread) = start_value_service();

        assert!(
            interface.options_receiver.try_recv().is_err(),
            "Controller should not send options until requested"
        );

        interface
            .service_message_sender
            .send(ServiceMessage::SendOptions)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.options_receiver.try_recv().is_ok(),
            "Controller should send options when requested"
        );
    }

    #[test]
    fn test_controller_message_send_debug() {
        let (interface, _thread) = start_value_service();

        assert!(
            interface.debug_receiver.try_recv().is_err(),
            "Controller should not send debug until requested"
        );

        interface
            .service_message_sender
            .send(ServiceMessage::SendDebug)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.debug_receiver.try_recv().is_ok(),
            "Controller should send debug when requested"
        );
    }

    #[test]
    fn test_controller_message_output_when_input() {
        let (interface, _thread) = start_value_service();

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output until it is provided input"
        );

        interface.initialization_input_sender.send(0).unwrap();
        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnZero)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv() == Ok(0),
            "Controller should provide output after it is sent input"
        );
    }

    #[test]
    fn test_controller_initialize_uninitialize() {
        let (interface, _thread) = start_value_service();

        interface
            .service_message_sender
            .send(ServiceMessage::SendDebug)
            .unwrap();

        sleep(Duration::from_millis(100));

        let output = interface.debug_receiver.try_recv();
        assert!(
            output.is_ok(),
            "Controller should provide debug info on request"
        );
        assert!(
            !output.unwrap().initialized,
            "Controller should not initialize until directed"
        );

        interface.initialization_input_sender.send(0).unwrap();

        sleep(Duration::from_millis(100));

        interface
            .service_message_sender
            .send(ServiceMessage::SendDebug)
            .unwrap();

        sleep(Duration::from_millis(100));

        let output = interface.debug_receiver.try_recv();
        assert!(
            output.is_ok(),
            "Controller should provide debug info on request"
        );
        assert!(
            output.unwrap().initialized,
            "Controller should initialize when directed"
        );

        interface
            .service_message_sender
            .send(ServiceMessage::Uninitialize)
            .unwrap();
        interface
            .service_message_sender
            .send(ServiceMessage::SendDebug)
            .unwrap();

        sleep(Duration::from_millis(100));

        let output = interface.debug_receiver.try_recv();
        assert!(
            output.is_ok(),
            "Controller should provide debug info on request"
        );
        assert!(
            !output.unwrap().initialized,
            "Controller should uninitialize when directed"
        );
    }

    #[test]
    fn test_controller_message_end() {
        let (interface, thread) = start_value_service();

        interface
            .service_message_sender
            .send(ServiceMessage::End)
            .unwrap();

        thread.join().unwrap();

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output after end"
        );
        assert!(
            interface.options_receiver.try_recv().is_err(),
            "Controller should not provide options after end"
        );
        assert!(
            interface.debug_receiver.try_recv().is_err(),
            "Controller should not provide debug after end"
        );
    }

    #[test]
    fn test_controller_no_input_without_initialization() {
        let (interface, _thread) = start_value_service();

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnZero)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output without initialization"
        );
    }

    #[test]
    fn test_controller_change_options() {
        let (interface, _thread) = start_value_service();

        interface
            .service_message_sender
            .send(ServiceMessage::SendOptions)
            .unwrap();

        sleep(Duration::from_millis(100));

        let mut options = interface.options_receiver.try_recv().unwrap();
        assert!(
            !options.paused,
            "Controller should not be paused by default"
        );
        options.paused = true;
        interface.options_sender.send(options).unwrap();

        sleep(Duration::from_millis(100));

        interface
            .service_message_sender
            .send(ServiceMessage::SendOptions)
            .unwrap();

        sleep(Duration::from_millis(100));

        let options = interface.options_receiver.try_recv().unwrap();
        assert!(options.paused, "Controller should be paused when requested");
    }

    #[test]
    fn test_controller_no_output_until_input() {
        let (interface, _thread) = start_value_service();

        interface.initialization_input_sender.send(0).unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output until it is provided input"
        );

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnZero)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv() == Ok(0),
            "Controller should provide output after it is sent input"
        );
    }

    #[test]
    fn test_controller_no_output_when_paused() {
        let (interface, _thread) = start_value_service();

        interface.initialization_input_sender.send(0).unwrap();

        sleep(Duration::from_millis(100));

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnZero)
            .unwrap();
        interface
            .service_message_sender
            .send(ServiceMessage::SendOptions)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv() == Ok(0),
            "Controller should provide output when not paused"
        );

        let mut options = interface.options_receiver.try_recv().unwrap();
        assert!(
            !options.paused,
            "Controller should not be paused by default"
        );
        options.paused = true;
        interface.options_sender.send(options).unwrap();

        sleep(Duration::from_millis(100));

        interface
            .service_message_sender
            .send(ServiceMessage::SendOptions)
            .unwrap();

        sleep(Duration::from_millis(100));

        let options = interface.options_receiver.try_recv().unwrap();
        assert!(options.paused, "Controller should be paused when requested");

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnZero)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output when paused"
        );
    }

    #[test]
    fn test_controller_each_input_produces_one_output() {
        let (interface, _thread) = start_value_service();

        interface.initialization_input_sender.send(0).unwrap();

        sleep(Duration::from_millis(100));

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnZero)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv() == Ok(0),
            "Controller should provide output after it is sent input"
        );

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should only provide one output per input"
        );
    }

    #[test]
    fn test_controller_no_initialization_when_initialized() {
        let (interface, _thread) = start_value_service();

        interface.initialization_input_sender.send(1).unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output until it is provided input"
        );

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnInitial)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv() == Ok(1),
            "Controller should provide output after it is sent input"
        );

        interface.initialization_input_sender.send(2).unwrap();

        sleep(Duration::from_millis(100));

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnInitial)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv() == Ok(1),
            "Controller should not re-initialize when provided second initialization"
        );
    }

    #[test]
    fn test_controller_no_step_when_not_initialized() {
        let (interface, _thread) = start_value_service();

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnZero)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output when not initialized"
        );

        interface
            .service_message_sender
            .send(ServiceMessage::Step)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output (even from step) when not initialized"
        );
    }

    #[test]
    fn test_controller_message_step() {
        let (interface, _thread) = start_value_service();

        interface.initialization_input_sender.send(0).unwrap();

        interface
            .service_message_sender
            .send(ServiceMessage::SendOptions)
            .unwrap();

        sleep(Duration::from_millis(100));

        let mut options = interface.options_receiver.try_recv().unwrap();
        assert!(
            !options.paused,
            "Controller should not be paused by default"
        );
        options.paused = true;
        interface.options_sender.send(options).unwrap();

        sleep(Duration::from_millis(100));

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnZero)
            .unwrap();

        sleep(Duration::from_millis(100));

        interface
            .service_message_sender
            .send(ServiceMessage::Step)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_ok(),
            "Controller should provide output from step even when paused"
        );

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Step should only produce one output"
        );
    }

    #[test]
    fn test_controller_no_step_without_input() {
        let (interface, _thread) = start_value_service();

        interface.initialization_input_sender.send(0).unwrap();

        interface
            .service_message_sender
            .send(ServiceMessage::SendOptions)
            .unwrap();

        sleep(Duration::from_millis(100));

        let mut options = interface.options_receiver.try_recv().unwrap();
        assert!(
            !options.paused,
            "Controller should not be paused by default"
        );
        options.paused = true;
        interface.options_sender.send(options).unwrap();

        sleep(Duration::from_millis(100));

        interface
            .service_message_sender
            .send(ServiceMessage::Step)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output if no input has ever been provided"
        );
    }

    #[test]
    fn test_controller_only_provides_latest_input() {
        let (interface, _thread) = start_value_service();

        interface.initialization_input_sender.send(1).unwrap();

        interface
            .service_message_sender
            .send(ServiceMessage::SendOptions)
            .unwrap();

        sleep(Duration::from_millis(100));

        let mut options = interface.options_receiver.try_recv().unwrap();
        assert!(
            !options.paused,
            "Controller should not be paused by default"
        );
        options.paused = true;
        interface.options_sender.send(options).unwrap();

        sleep(Duration::from_millis(100));

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnZero)
            .unwrap();

        interface
            .input_sender
            .send(ValueServiceInstructions::ReturnInitial)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv().is_err(),
            "Controller should not provide output until step is requested"
        );

        interface
            .service_message_sender
            .send(ServiceMessage::Step)
            .unwrap();

        sleep(Duration::from_millis(100));

        assert!(
            interface.output_receiver.try_recv() == Ok(1),
            "Controller should provide output from latest input"
        );
    }
}
