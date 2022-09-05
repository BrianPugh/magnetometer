from math import pi, sin

from .base import Sensor


class Sin(Sensor):
    def __init__(self, port, sda, scl):
        """Dummy sinusoidal sensor for debugging purposes."""
        self.read = self.init_sensor()

    def init_sensor(self):
        i = 0

        def read(scale=0):
            nonlocal i
            out = (
                1 + sin(2 * pi * (0.1 * i) + 0.0),
                0 + sin(2 * pi * (0.1 * i) + 2.0),
                -1 + sin(2 * pi * (0.1 * i) + 4.0),
            )
            i += 1
            return out

        return read
