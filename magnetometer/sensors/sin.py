from math import pi, sin

from .base import Sensor


class Sin(Sensor):
    def __init__(self, port, sda, scl):
        """Dummy sinusoidal sensor for debugging purposes."""
        self.i = 0

    @staticmethod
    def init_sensor():
        pass

    def read(self, scale=0, samples=16):
        out = (
            1 + sin(2 * pi * (0.1 * self.i) + 0.0),
            0 + sin(2 * pi * (0.1 * self.i) + 2.0),
            -1 + sin(2 * pi * (0.1 * self.i) + 4.0),
        )
        self.i += 1
        return out
