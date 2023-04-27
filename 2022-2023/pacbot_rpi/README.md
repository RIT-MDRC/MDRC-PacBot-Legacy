# Working with the Raspberry Pi

## Boot

- The Pi should boot into Ubuntu Desktop 22.10 when it receives power via the USB-C port
- If a display is plugged in, it will show the desktop (login is disabled)
- When it boots up, the pi will:
  - Attempt to connect to Wifi (like a regular computer, uses saved networks)
  - Launch its remote.it client

## Access

- The ability to connect to the pi is determined by what internet it is connected to
- For all connection types, the username is `pi` and the password is `raspberry`
  - RIT Wifi: `ssh pi@mdrcpi4.student.rit.edu`
  - Remote.it: Use the provided SSH command
  - Other wifi networks: It is recommended to connect with Remote.it to acquire the IP, then if desired, connect using the IP
- The pi currently does not support remote desktop access

## Organization

- The main `MDRC-PacBot` repository is located at `~/MDRC-PacBot`
- The `mdrc-pacbot-rl` repository, which includes the Rust source code, is located at `~/mdrc-pacbot-rl`

## Compilation/Setup

- Note that some utilities might only be installed for the `pi` user
- To compile the Rust code
  - Go to the mdrc-pacbot-rl directory
    - `cd ~/mdrc-pacbot-rl`
  - Ensure you are on the right branch
    - `git checkout michael-rust-pf`
  - Start a poetry shell
    - `poetry shell`
  - Go to the rust directory
    - `cd ~/mdrc-pacbot-rl/pacbot_rs`
  - Compile the rust code
    - To compile as a wheel
      - `maturin build --release`
      - `exit` (to exit poetry shell)
      - (enter whichever virtualenv you want to use, or use the global one)
      - `python3 -m pip uninstall pacbot_rs -y`
      - `python3 -m pip install ~/mdrc-pacbot-rl/pacbot_rs/target/wheels/*`
    - To compile into the Poetry virtualenv
      - `maturin develop --release`
- To install the necessary Python packages
  - `python3 -m pip install -r ~/MDRC-PacBot/2022-2023/pacbot_rpi/requirements.txt`
- To install new code on the Arduino, use the Arduino IDE to connect via USB-B and upload there
  - The arduino automatically executes its code when it receives power

## Architecture

This project exists in 5 parts.

1. Server
   - The server handles game ticks, ghost movement, and other game engine tasks
2. Rust code, `mdrc-pacbot-rl`
   - This code handles particle filter and heuristic calculations
   - See compilation process above
3. Python code, `pacbot_rpi`
   - This is the code that manages Pacbot tasks such as arduino communication and server communication
   - This code spawns one Python thread in addition to the main thread that is responsible for server communication
4. Arduino code
   - This is the low-level code that runs on the Arduino, which communicates with the Python code via the serial port
5. The Projector
   - The projector attempts to determine Pacbot's position using computer vision, and sends messages to MsgType.PACMAN_LOCATION for the server

## The Server

The server, whether it is running on your machine or Harvard's, can be composed of several processes as follows.
Each component is one of the python files in `Pacbot/src/gameEngine/`
1. gameEngine - required, keeps track of the current game state
   - Listens for messages from PACMAN_LOCATION
   - Sends messages to FULL_STATE, LIGHT_STATE
2. cameraReader - optional, uses computer vision to track Pacbot
   - Sends messages to PACMAN_LOCATION
   - If it doesn't exist, pacbot needs to send messages to PACMAN_LOCATION
3. keyboardInput - provides a way to control game engine's pacman via keyboard
   - Sends messages to PACMAN_LOCATION
   - If it exists, the physical robot's Pacbot code should not exist
4. server - required, is simply the Robomodules serverside, all other processes are a client
   - Does not send any messages
5. terminalPrinter - optional, this thing has never worked for me
6. visualize - provides a Pygame visualization of the game state

All server processes accept the following environment variables, which must match for all processes.
If `localhost` is the `BIND_ADDRESS`, no process outside the machine running the server will be able to access it.
- `BIND_ADDRESS`
  - Default: `localhost`
- `BIND_PORT`
  - Default: `11297`

An easy to manage the server is to use `python3 ~/MDRC-PacBot/2022-2023/auto_robo/auto_robo.py`

Auto robo also accepts BIND_ADDRESS and BIND_PORT, which are passed into each process. 

In order to run auto robo, make sure you have `python3 -m pip install -r ~/MDRC-PacBot/2022-2023/auto_robo/requirements.txt`