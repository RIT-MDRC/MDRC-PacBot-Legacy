from simulator import Controller, MAX_DISTANCE


class PDController(Controller):
    def __init__(self) -> None:
        super().__init__()

        self.P = MAX_DISTANCE * 0.3 * 5
        self.D = 1

        self.last_error = None

    def step(self, dt, sensor_values) -> tuple[float, float]:
        left_sensor = sensor_values[0]
        right_sensor = sensor_values[-1]

        error = left_sensor - right_sensor
        if self.last_error is None:
            d_error = 0
        else:
            d_error = (error - self.last_error) / dt
        self.last_error = error

        steer = -(error * self.P) - (d_error * self.D)
        left_motor = 1.0 + steer
        right_motor = 1.0 - steer
        return left_motor, right_motor
