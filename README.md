# Magnetometer

This is a [magnetometer](https://en.wikipedia.org/wiki/Magnetometer) command-line tool that reads from physical magnetic sensors via
[Belay](https://github.com/BrianPugh/belay).

<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/14318576/187823929-9b6985e7-4124-49b1-9e13-6268ee155d92.gif">
</p>

# Installation
Install Magnetometer through pip:

```
pip install magnetometer
```

# Usage

To start the program, invoke `magnetometer` along with the port your
CircuitPython board is connected to.

```
magnetometer DEVICE_PORT --sensor SENSOR_TYPE
```

You can use the debugging sensor `sin` without any physical hardware interactions.
CircuitPython must be installed on-device and [must be configured with rw storage](https://belay.readthedocs.io/en/latest/CircuitPython.html).
Magnetometer will automatically upload all necessary code to device.
Run `magnetometer --help` to see more options.

<p align="center">
  <img width="600" src="https://user-images.githubusercontent.com/14318576/187825892-6e9594ec-9598-4aaa-9b00-fec3f82ae278.jpeg">
</p>

### Supported Sensors

* [LIS3MDL](https://www.adafruit.com/product/4479) - Up to ±1,600μT
* [MMC5603](https://www.adafruit.com/product/5579) - Up to ±3,000μT
* [LIS2MDL](https://www.adafruit.com/product/4488) - Up to ±5,000μT
* [TLV493D](https://www.adafruit.com/product/4366) - Up to ±130,000μT

Want to support another sensor? Open an issue (or even a PR) on Github and we
can try to add it!

# Acknowledgements
This tool uses many awesome libraries that keep the implementation terse and the outputs beautiful:
* [Belay](https://github.com/BrianPugh/belay) - Seameless python/hardware interactions. Used for all hardware interactions.
* [AutoRegistry](https://github.com/BrianPugh/autoregistry) - Automatic registry design-pattern library for mapping names to functionality. Used to manage sensor hardware abstraction layer.
* [Textual](https://github.com/Textualize/textual) - Text User Interface framework for Python inspired by modern web development. Used for dynamic user input.
* [Rich](https://github.com/Textualize/rich) - Python library for rich text and beautiful formatting in the terminal. Used for general UI text rendering.
* [AsciiChartPy](https://github.com/kroitor/asciichart) - Nice-looking lightweight console ASCII line charts. Used for chart plotting. Modified to be `rich`-compatible.
