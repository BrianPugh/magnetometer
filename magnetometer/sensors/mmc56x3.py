from .base import Sensor


class MMC5603(Sensor):
    scales = [3000]

    @Sensor.setup(autoinit=True)
    def init_sensor():
        from adafruit_mmc56x3 import MMC5603

        sensor = MMC5603(i2c)
        sensor.data_rate = 1000
        sensor.continuous_mode = True
        sensor

    @Sensor.task
    def read(scale=0, samples=16):
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
