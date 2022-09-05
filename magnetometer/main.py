from __future__ import annotations

from collections import deque
from enum import Enum
from functools import partial
from math import isfinite, nan, sqrt
from pathlib import Path
from typing import Optional

import typer
from rich.columns import Columns
from rich.console import Group, RenderableType
from rich.panel import Panel
from textual.app import App
from textual.widget import Widget
from textual.widgets import Footer
from typer import Argument, Option

import magnetometer.asciichartpy as acp
from magnetometer import Sensor, __version__

app = typer.Typer()

Arg = partial(Argument, ..., show_default=False)
Opt = partial(Option)
SensorEnum = Enum("SensorEnum", {k: k for k in Sensor}, type=str)

sensor: Sensor

X_COLOR = "red"
Y_COLOR = "green"
Z_COLOR = "blue"
MAG_COLOR = "white"


class Chart(Widget):
    def on_mount(self) -> None:
        history_length = 1024

        self.height = -1
        self.width = -1

        self.zero_x_val = 0
        self.zero_y_val = 0
        self.zero_z_val = 0

        self.scale = 0

        # Add a dummy zero-value to simulate an X-axis
        self.history = deque(
            [(0, nan, nan, nan, nan)] * history_length, maxlen=history_length
        )
        self.history.append((0, 0, 0, 0, 0))  # Need one valid data-point
        self.set_interval(0.1, self.read_sensor)

    def zero_x(self) -> None:
        self.zero_x_val += self.history[-1][1]

    def zero_y(self) -> None:
        self.zero_y_val += self.history[-1][2]

    def zero_z(self) -> None:
        self.zero_z_val += self.history[-1][3]

    def read_sensor(self) -> None:
        x, y, z = sensor.read(self.scale)

        x -= self.zero_x_val
        y -= self.zero_y_val
        z -= self.zero_z_val
        mag = sqrt(x**2 + y**2 + z**2)

        # Auto-scale logic
        threshold = 0.9
        if sensor.scales:
            max_mag = max(x, y, z)
            lower_scale = max(0, self.scale - 1)
            new_scale = self.scale
            if max_mag > threshold * sensor.scales[self.scale]:
                new_scale = min(len(sensor.scales) - 1, self.scale + 1)
            elif max_mag < threshold * sensor.scales[lower_scale]:
                new_scale = lower_scale

            if new_scale != self.scale:
                self.scale = new_scale

        self.history.append((0, x, y, z, mag))
        self.refresh()

    def on_resize(self, event):
        self.height = event.height
        self.width = event.width

    def render(self) -> RenderableType:
        if self.height == -1 or self.width == -1:
            return ""

        width = self.width - 13
        cfg = {
            "offset": 2,
            "colors": ["", X_COLOR, Y_COLOR, Z_COLOR, MAG_COLOR],
            "height": self.height - 5,
        }

        series = [list(elem)[-width:] for elem in zip(*self.history)]
        max_mag = max(mag for mag in series[4] if isfinite(mag))

        if max_mag > 1000:
            units = "m"
            series = [[x / 1000 for x in data] for data in series]
        else:
            units = "μ"

        x = series[1][-1]
        y = series[2][-1]
        z = series[3][-1]
        mag = series[4][-1]

        buf = acp.plot(series, cfg)

        return Group(
            Panel(
                buf,
                title=f"Magnetometer v{__version__} ({sensor.__registry__.name})",
            ),
            Columns(
                [
                    f"[bold {X_COLOR}]X: {x:6.2f} {units}T[/]",
                    f"[bold {Y_COLOR}]Y: {y:6.2f} {units}T[/]",
                    f"[bold {Z_COLOR}]Z: {z:6.2f} {units}T[/]",
                    f"[bold {MAG_COLOR}]Mag: {mag:6.2f} {units}T[/]",
                ],
                equal=True,
                expand=True,
                align="center",
            ),
        )


class MagnetometerApp(App):
    async def on_load(self) -> None:
        await self.bind("a", "zero_all", "Zero ALL")
        await self.bind("x", "zero_x", "Zero X")
        await self.bind("y", "zero_y", "Zero Y")
        await self.bind("z", "zero_z", "Zero Z")

        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        footer = Footer()
        self.chart = Chart()

        await self.view.dock(footer, edge="bottom")
        await self.view.dock(self.chart, edge="top")

    def action_zero_x(self) -> None:
        self.chart.zero_x()

    def action_zero_y(self) -> None:
        self.chart.zero_y()

    def action_zero_z(self) -> None:
        self.chart.zero_z()

    def action_zero_all(self) -> None:
        self.chart.zero_x()
        self.chart.zero_y()
        self.chart.zero_z()


def version_callback(value: bool):
    if value:
        print(__version__)
        raise typer.Exit()


@app.command()
def main(
    port: str = Arg(help="CircuitPython device communication port."),
    sda: int = Opt(0, help="Device I2C SDA GPIO number."),
    scl: int = Opt(1, help="Device I2C SDA GPIO number."),
    sensor_name: SensorEnum = Opt(
        "lis3mdl", "--sensor", case_sensitive=False, help="Sensor Type."
    ),
    version: Optional[bool] = Opt(
        None, "--version", callback=version_callback, help="Print Magnetometer version."
    ),
    log: Path = Opt("", help="Filename to write debugging logs."),
):
    global sensor
    sensor = Sensor[sensor_name.value](port, sda, scl)

    log: str = str(log)
    if log == ".":
        log = ""
    MagnetometerApp.run(log=log)
