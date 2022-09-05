from .base import Sensor


class LIS3MDL(Sensor):
    scales = [400, 800, 1200, 1600]

    def init_sensor(self):
        self.device("from adafruit_lis3mdl import LIS3MDL")
        self.device("sensor = LIS3MDL(i2c)")

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
            # LIS3MDL in this mode samples at 115Hz
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
