from abc import abstractmethod
from typing import Callable, Tuple

from autoregistry import Registry
from belay import Device


class Sensor(Device, Registry):
    # If Sensor has multiple measurement ranges, describe them here.
    # In microteslas.
    scales: list = []

    def __init__(self, *args, scl, sda, **kwargs):
        self.scl = scl
        self.sda = sda
        super().__init__(*args, **kwargs)

    def __pre_autoinit__(self):
        if self.implementation.name != "circuitpython":
            raise RuntimeError(
                f"Board must be running CircuitPython, detected {self.implementation.name}."
            )
        self.sync_dependencies("magnetometer", "dependencies/main")
        self("from busio import I2C; import board")
        self(f"i2c = I2C(board.GP{self.scl}, board.GP{self.sda})")

    @abstractmethod
    def init_sensor() -> None:
        raise NotImplementedError

    @abstractmethod
    def read(scale=0, samples=16) -> Tuple[float, float, float]:
        """Read sensor on-device.

        The object ``i2c`` is already initialized on-device.

        Parameters
        ----------
        scale : int
            Index into gauss range scale.
            May or may not be used depending on sensor.
        samples: int
            Number of samples to average together per reading (oversampling).

        Returns
        -------
        Tuple[float, float, float]
            (x, y, z) magnetic reading in microteslas.
        """

        raise NotImplementedError
