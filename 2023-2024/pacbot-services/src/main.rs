use log::warn;

mod model;
mod service;

fn main() {
    println!("Hello, world!");

    log4rs::init_file("log4rs.yml", Default::default()).unwrap();

    warn!("oops!");
}
