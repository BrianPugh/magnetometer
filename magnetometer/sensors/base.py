from abc import abstractmethod
from typing import Callable, Tuple

import pkg_resources
from autoregistry import Registry
from belay import Device


class Sensor(Registry):
    read: Callable[..., Tuple[float, float, float]]

    # If Sensor has multiple measurement ranges, describe them here.
    # In microteslas.
    scales: list = []

    def __init__(self, port, sda, scl):
        self.device = Device(port)
        if self.device.implementation.name != "circuitpython":
            raise RuntimeError(
                f"Board must be running CircuitPython, detected {self.device.implementation.name}."
            )

        board_path = pkg_resources.resource_filename("magnetometer", "board")
        self.device.sync(board_path)

        self.device(f"i2c = I2C(board.GP{scl}, board.GP{sda})")
        self.read = self.init_sensor()

    @abstractmethod
    def init_sensor(self) -> Callable[..., Tuple[float, float, float]]:
        """Initialize sensor on-device and prepares ``read_sensor`` task.

        The object ``i2c`` is already initialized on-device.

        Returns
        -------
        Callable[..., Tuple[float, float, float]]
            Function that will read sensor and return an (x, y, z)
            magnetic reading in microteslas.
        """
        raise NotImplementedError
