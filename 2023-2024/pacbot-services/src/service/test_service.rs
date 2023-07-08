use crate::service::service_controller::{
    Service, ServiceDebugEntry, ServiceDebugGroup, ServiceOption, ServiceOptionGroup,
};

enum TestServiceOperations {
    Add,
    Subtract,
    Multiply,
    Divide,
}

pub struct TestService {
    initialization_input: u32,
    options: TestServiceOptions,

    last_input: [u32; 2],
}

pub struct TestServiceInitializationInput {
    number: u32,
}

pub struct TestServiceInput {
    inputs: [u32; 2],
    operation: TestServiceOperations,
}

pub struct TestServiceOutput {
    output: f32,
}

pub struct TestServiceOptions {
    number: u32,
}

impl TestService {
    pub fn new() -> Self {
        Self {
            initialization_input: 0,
            options: TestServiceOptions { number: 0 },

            last_input: [0, 0],
        }
    }
}

impl Service<TestServiceInitializationInput, TestServiceInput, TestServiceOutput> for TestService {
    fn get_options(&self) -> ServiceOptionGroup {
        ServiceOptionGroup {
            options: vec![ServiceOption::UnsignedNumber(
                "test option 1".to_string(),
                0,
            )],
        }
    }

    fn get_debug(&self) -> ServiceDebugGroup {
        ServiceDebugGroup {
            debug: vec![
                ServiceDebugEntry::Int("debug 1".to_string(), self.last_input[0] as i32),
                ServiceDebugEntry::Int("debug 2".to_string(), self.last_input[1] as i32),
            ],
        }
    }

    fn get_default_input(&self) -> TestServiceInput {
        TestServiceInput {
            inputs: [0, 0],
            operation: TestServiceOperations::Add,
        }
    }

    fn set_options(&mut self, options: &ServiceOptionGroup) {
        if let ServiceOption::UnsignedNumber(_, value) = &options.options[0] {
            self.options.number = *value;
        }
    }

    fn initialize(
        &mut self,
        initialization_values: TestServiceInitializationInput,
    ) -> Result<(), String> {
        self.initialization_input = initialization_values.number;

        Ok(())
    }

    fn step(&mut self, input_values: &TestServiceInput) -> Result<TestServiceOutput, String> {
        let first_input = input_values.inputs[0] as f32;
        let second_input = input_values.inputs[1] as f32;

        self.last_input = input_values.inputs;

        match &input_values.operation {
            TestServiceOperations::Add => Ok(TestServiceOutput {
                output: first_input + second_input,
            }),
            TestServiceOperations::Subtract => Ok(TestServiceOutput {
                output: first_input - second_input,
            }),
            TestServiceOperations::Multiply => Ok(TestServiceOutput {
                output: first_input * second_input,
            }),
            TestServiceOperations::Divide => {
                if second_input != 0 as f32 {
                    Ok(TestServiceOutput {
                        output: first_input / second_input,
                    })
                } else {
                    Err("cannot divide by 0".to_string())
                }
            }
        }
    }

    fn uninitialize(&mut self) {
        self.initialization_input = 0;

        self.last_input = [0, 0];
    }
}
