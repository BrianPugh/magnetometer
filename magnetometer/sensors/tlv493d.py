from .base import Sensor


class TLV493D(Sensor):
    scales = [130_000]

    def init_sensor(self):
        self.device("from adafruit_tlv493d import TLV493D")
        self.device("sensor = TLV493D(i2c)")

        @self.device.task
        def read(scale=0, samples=16):
            """Read sensor-measured magnetic field.

            Parameters
            ----------
            scale : int
                One of ``{0, 1, 2, 3}``, representing  ``{4, 8, 12, 16}`` gauss ranges.

            Returns
            -------
            tuple
                (x, y, z) magnetic field in microteslas.
            """
            sensor.range = scale  # noqa: F821
            x_avg, y_avg, z_avg = 0, 0, 0
            for _ in range(samples):
                x, y, z = sensor.magnetic  # noqa: F821
                x_avg += x
                y_avg += y
                z_avg += z
            x_avg /= samples
            y_avg /= samples
            z_avg /= samples
            return (x_avg, y_avg, z_avg)

        return read
