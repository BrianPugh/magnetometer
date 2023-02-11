from .base import Sensor


class TLV493D(Sensor):
    scales = [130_000]

    @Sensor.setup(autoinit=True)
    def init_sensor():
        from adafruit_tlv493d import TLV493D

        sensor = TLV493D(i2c)

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
