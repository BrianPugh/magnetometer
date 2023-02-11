from .base import Sensor


class LIS2MDL(Sensor):
    scales = [5000]

    @Sensor.setup(autoinit=True)
    def init_sensor():
        from adafruit_lis2mdl import LIS2MDL, DataRate

        sensor = LIS2MDL(i2c)
        sensor.low_power = 0  # High Resolution
        sensor.data_rate = DataRate.Rate_100_HZ

    @Sensor.task
    def read(scale=0, samples=16):
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
