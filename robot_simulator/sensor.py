import math

c1 = 3.91166
c2 = 0.395185
c3 = -0.942507


def distance_to_voltage(distance: float):
    return c3 - c2 / math.pow(distance, c2)


def voltage_to_distance(voltage: float):
    return math.pow((voltage - c3) / c1, 1 / -c2)
