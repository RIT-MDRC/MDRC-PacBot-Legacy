from typing import NamedTuple
from bot_math import Pose, Position
import pacbot_rs


class OutgoingArduinoMessage(NamedTuple):
    """The message sent from the Raspberry Pi to the Arduino."""
    # The message is a 5-byte string, with the first byte being the command 's' or 't'
    # and the other 4 bytes being the integer argument
    command: str
    argument: int  # if command == 't', this is the angle in degrees from -180 to 180

    def format(self):
        """Returns a string of the message formatted for printing."""
        return f"{self.command} {self.argument}\n"


class IncomingArduinoMessage:
    """The message sent from the Arduino to the Raspberry Pi."""
    # The message is a string of the two parts separated by a semicolon:
    # - two floating point encoder values, separated by a comma
    # - five floating point IR sensor values, separated by commas
    encoder_values: tuple[float, float]
    ir_sensor_values: tuple[float, float, float, float, float]

    def __init__(self, e, i):
        self.encoder_values = e
        self.ir_sensor_values = i


def str_to_incoming_message(message_bytes: str) -> IncomingArduinoMessage:
    """Converts a message from the Arduino to an IncomingArduinoMessage object."""
    message = message_bytes
    encoder_values, ir_sensor_values = message.split(";")
    encoder_values = tuple(float(value) for value in encoder_values.split(","))
    ir_sensor_values = tuple(float(value) for value in ir_sensor_values.split(","))
    return IncomingArduinoMessage(encoder_values, ir_sensor_values)


class DebugFrame(NamedTuple):
    """
    A debug frame, containing information about the game.
    """
    # environment
    USE_REAL_ARDUINO: bool
    USE_PROJECTOR: bool
    ADDRESS: str
    PORT: int

    # server
    game_state: pacbot_rs.GameState

    # simulated
    pacbot_pose: Pose
    pacbot_pose_sensor_readings: list[float]

    pf_points: list[tuple[tuple[float, float], float]]
    pf_map_segments: list[tuple[int, int, int, int]]
    pf_empty_grid_cells: list[tuple[int, int]]

    target_pos: Position
    target_path: list[Position]

    pp_speed: float
    pp_angle: float
    pp_left_motor: float
    pp_right_motor: float

    # measured
    encoder_readings: tuple[float, float]
    ir_sensor_readings: list[float]

    lines_read: list[IncomingArduinoMessage]
    lines_sent: list[OutgoingArduinoMessage]
