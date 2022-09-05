from .base import Sensor


class LIS2MDL(Sensor):
    scales = [5000]

    def init_sensor(self):
        self.device("from adafruit_lis2mdl import LIS2MDL, DataRate")
        self.device("sensor = LIS2MDL(i2c)")
        self.device("sensor.low_power = 0")  # High Resolution
        self.device("sensor.data_rate = DataRate.Rate_100_HZ")

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
